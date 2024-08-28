import time
import mysql.connector
import geopandas as gpd
import pandas as pd
import sys
import os
from tqdm import tqdm
import logging
from shapely import wkt
import hashlib
import traceback
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

# Use a projected CRS for centroid calculation
PROJ_CRS = 'EPSG:3395'  # World Mercator projected CRS

def detect_outliers(df, column):
    Q1 = df[column].quantile(0.05)
    Q3 = df[column].quantile(0.95)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (df[column] < lower_bound) | (df[column] > upper_bound)

def simplify_polygon(geom, tolerance=0.0001):
    if geom.geom_type == 'Polygon':
        simplified = geom.simplify(tolerance, preserve_topology=True)
        return simplified if not simplified.is_empty else geom
    elif geom.geom_type == 'MultiPolygon':
        simplified_parts = [part.simplify(tolerance, preserve_topology=True) for part in geom.geoms]
        non_empty_parts = [part for part in simplified_parts if not part.is_empty]
        return geom if len(non_empty_parts) == 0 else MultiPolygon(non_empty_parts)
    else:
        return geom

def prepare_and_load_aux_data(file_path):
    start_time = time.time()

    try:
        # Initialize the database model
        db_model = ForestModel(mysql_params)

        # Check if forest_aux table exists, if not create it
        db_model.create_forest_aux()
        logging.info("Ensured forest_aux table exists.")

        # Read the GIS file into a GeoDataFrame
        gdf = gpd.read_file(file_path)
        logging.info("Data loaded successfully.")
        logging.info(f"Columns in the GeoDataFrame: {gdf.columns}")
        logging.info(f"First few rows: {gdf.head()}")

        # Check and convert to WGS84 if needed
        if gdf.crs != 'epsg:4326':
            gdf = gdf.to_crs(epsg=4326)
        logging.info("CRS conversion completed.")

        # Project to a suitable local projection for accurate area calculation
        local_crs = pyproj.CRS.from_epsg(3857)  # Web Mercator projection
        gdf = gdf.to_crs(local_crs)

        # Calculate original areas
        gdf['original_area'] = gdf.geometry.area

        # Simplify geometries
        gdf['simplified_geometry'] = gdf.geometry.apply(lambda geom: simplify_polygon(geom, tolerance=10))  # 10 meters tolerance

        # Calculate simplified areas
        gdf['simplified_area'] = gdf.simplified_geometry.area

        # Check for significant area changes
        gdf['area_change'] = (gdf['original_area'] - gdf['simplified_area']) / gdf['original_area']

        # If area change is too large, revert to original geometry
        gdf.loc[gdf['area_change'] > 0.1, 'simplified_geometry'] = gdf.loc[gdf['area_change'] > 0.1, 'geometry']

        # Replace the original geometry with the simplified one
        gdf['geometry'] = gdf['simplified_geometry']

        # Project back to WGS84
        gdf = gdf.to_crs('epsg:4326')

        # Remove temporary columns
        gdf = gdf.drop(columns=['original_area', 'simplified_area', 'area_change', 'simplified_geometry'])

        # Calculate centroids
        gdf['centroide_lat_wgs84'] = gdf.geometry.centroid.y
        gdf['centroide_lng_wgs84'] = gdf.geometry.centroid.x

        # Convert geometry to WKT
        gdf['polygon'] = gdf.geometry.apply(lambda geom: geom.wkt if geom.is_valid else None)

        logging.info("Geometry simplification and conversion to WKT completed.")

        # Add the tree type and filter out rows where 'tipo_id' is 0
        logging.info(f"Columns in the GeoDataFrame: {gdf.columns}")
        if 'FORARB' in gdf.columns:
            logging.info(f"First few rows of 'FORARB' column: {gdf['FORARB'].head()}")
            gdf['tipo_id'] = gdf['FORARB']
        else:
            logging.error("'FORARB' column not found in the GeoDataFrame")
            raise KeyError("'FORARB' column not found")

        if 'FormArbol' in gdf.columns:
            gdf['tipo_desc'] = gdf['FormArbol']
        else:
            logging.error("'FormArbol' column not found in the GeoDataFrame")
            raise KeyError("'FormArbol' column not found")

        gdf = gdf[gdf['tipo_id'] != 0]

        # Now create the location_id
        def create_efficient_location_id(row):
            try:
                base = f"{row['tipo_id']}_{row['centroide_lat_wgs84']:.5f}_{row['centroide_lng_wgs84']:.5f}"
                return hashlib.md5(base.encode()).hexdigest()[:12]
            except KeyError as e:
                logging.error(f"KeyError in create_efficient_location_id: {e}")
                logging.error(f"Available columns: {row.index}")
                raise

        gdf['location_id'] = gdf.apply(create_efficient_location_id, axis=1)
        logging.info("Location ID creation completed.")

        # Detect outliers
        lat_outliers = detect_outliers(gdf, 'centroide_lat_wgs84')
        lon_outliers = detect_outliers(gdf, 'centroide_lng_wgs84')
        outliers = gdf[lat_outliers | lon_outliers]
        if not outliers.empty:
            logging.warning("Outliers detected:")
            logging.warning(outliers[['centroide_lat_wgs84', 'centroide_lng_wgs84']])
            # Consider how you want to handle outliers (e.g., remove them or flag them)

        # Remove outliers
        gdf = gdf[~(lat_outliers | lon_outliers)]

        # Insert data into the auxiliary table
        try:
            data_tuples = []
            for _, row in tqdm(gdf.iterrows(), total=gdf.shape[0], desc='Preparing data for insertion'):
                if row['polygon'] is not None:
                    data_tuples.append((
                        row['tipo_id'],
                        row['tipo_desc'],
                        row['centroide_lat_wgs84'],
                        row['centroide_lng_wgs84'],
                        row['polygon'],
                        row['location_id']
                    ))
            logging.info(f"Total records to be inserted: {len(data_tuples)}")
            
            for batch_start in tqdm(range(0, len(data_tuples), 100), desc='Inserting data', unit='batch'):
                batch = data_tuples[batch_start:batch_start + 100]
                db_model.insert_forest_aux_bulk(batch, batch_size=100)

            logging.info("Data inserted into auxiliary table successfully.")
        except mysql.connector.Error as e:
            logging.error(f"Error while connecting or manipulating the database: {e}")
        finally:
            if db_model and db_model.conn.is_connected():
                db_model.conn.close()

        logging.info(f"Total time taken for data preparation and auxiliary table insertion: {time.time() - start_time} seconds")

    except Exception as e:
        logging.error(f"An error occurred during data processing: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise  # Re-raise the exception after logging

if __name__ == '__main__':
    file_path = r'C:\Users\mario\Downloads\mfe_madrid\MFE_30.shp'
    prepare_and_load_aux_data(file_path)