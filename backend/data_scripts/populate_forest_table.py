import time
import mysql.connector
import geopandas as gpd
import pandas as pd
import numpy as np
import sys
import os
from shapely.geometry import Polygon
import hashlib

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

# Usa un CRS proyectado para el cálculo del centroide
PROJ_CRS = 'EPSG:3395'  # Un CRS proyectado mundial como Mercator

def generate_forest_id(location_id):
    """Generate a unique weather_id based on location_id and date using MD5."""
    unique_string = f"{location_id}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def fetch_elevation_from_db(lat, lng, db_model):
    """Fetch elevation data from the database for the closest point to the given lat, lng."""
    query = f"""
        SELECT altitude FROM elevation_data
        ORDER BY ST_DISTANCE(POINT(latitude, longitude), POINT({lat}, {lng}))
        LIMIT 1
    """
    result = db_model.execute_query(query)
    if result:
        return result[0][0]
    return None

def prepare_data(file_path):
    start_time = time.time()

    # Read the GIS file into a GeoDataFrame
    gdf = gpd.read_file(file_path)
    print("Datos cargados correctamente.")
    print(f"Primeras geometrías: {gdf.geometry.head()}")

    # Check and convert to a projected CRS if it's not (e.g., EPSG:3857)
    start_crs_conversion_time = time.time()
    if gdf.crs != 'epsg:4326':
        gdf = gdf.to_crs(epsg=4326)
    print("Conversión de CRS realizada.")
    print(f"Time taken for CRS conversion: {time.time() - start_crs_conversion_time} seconds")

    # Cálculo de centroides utilizando vectorización
    start_centroid_calculation_time = time.time()
    gdf = gdf.to_crs(PROJ_CRS)
    centroids = gdf.centroid
    gdf['centroide_lat'] = centroids.y
    gdf['centroide_lng'] = centroids.x
    gdf = gdf.to_crs('epsg:4326')  # Volver al CRS original
    print("Cálculo de centroides realizado.")
    print(f"Time taken for centroid calculation: {time.time() - start_centroid_calculation_time} seconds")

    # Simplificación de polígonos y transformación en WKT
    start_wkt_conversion_time = time.time()
    gdf['polygon'] = gdf['geometry'].apply(lambda geom: geom.wkt if geom.is_valid else None)
    print("Conversión de geometrías a WKT realizada.")
    print(f"Time taken for WKT conversion: {time.time() - start_wkt_conversion_time} seconds")

    # Crear identificadores de ubicación
    start_location_id_time = time.time()
    gdf['location_id'] = gdf.apply(lambda row: f"{row['centroide_lat']}_{row['centroide_lng']}", axis=1)
    print("Creación de identificadores de ubicación realizada.")
    print(f"Time taken for location ID creation: {time.time() - start_location_id_time} seconds")

    # Add the tree type
    gdf['tipo_id'] = gdf['FORARB']
    gdf['tipo_desc'] = gdf['FormArbol']

    # Filter out rows where 'tipo_id' is 0
    gdf = gdf[gdf['tipo_id'] != 0]

    # Fetch elevation data from the database
    db_model = ForestModel(mysql_params)

    # Assign elevations to centroids
    start_elevation_time = time.time()
    locations = list(zip(gdf['centroide_lat'], gdf['centroide_lng']))
    gdf['altitude'] = [fetch_elevation_from_db(lat, lng, db_model) for lat, lng in locations]
    print("Asignación de datos de elevación realizada.")
    print(f"Time taken for elevation assignment: {time.time() - start_elevation_time} seconds")

    # Filter out rows where 'altitude' is less than 1000
    gdf = gdf[gdf['altitude'] > 2000]

    print(gdf[['tipo_id', 'tipo_desc', 'centroide_lat', 'centroide_lng', 'polygon', 'altitude', 'location_id']].head())

    print(f"Total time taken for data preparation: {time.time() - start_time} seconds")

    return gdf

def populate_forest_table():
    start_time = time.time()
    db_model = None

    # Path to the GIS file
    file_path = r'C:\Users\mario\Downloads\mfe_madrid\MFE_30.shp'

    # Prepare the data
    prepared_data = prepare_data(file_path)

    if not prepared_data.empty:
        try:
            # Initialize the model with the path to the database
            db_model = ForestModel(mysql_params)

            # Check for existing data in the table
            existing_data = db_model.fetch_existing_data(prepared_data['location_id'].tolist())

            # Filter out existing data
            new_data = prepared_data[~prepared_data['location_id'].isin(existing_data)]

            # Print count of new records to be inserted
            new_records_count = len(new_data)
            print(f"Number of new records to be inserted: {new_records_count}")

            # Insert data into the database in batches
            if not new_data.empty:
                start_insertion_time = time.time()
                data_tuples = []
                for _, row in new_data.iterrows():
                    row['forest_id'] = generate_forest_id(row['location_id'])
                    if row['polygon'] is not None:
                        data_tuples.append((
                            row['forest_id'],
                            row['tipo_id'],
                            row['tipo_desc'],
                            row['centroide_lat'],
                            row['centroide_lng'],
                            row['polygon'],  # Assuming this is already in WKT
                            row['altitude'],
                            row['location_id']
                        ))
                db_model.insert_forest_bulk(data_tuples, batch_size=100)  # Ajusta el tamaño del lote según sea necesario
                print("Data inserted successfully.")
                print(f"Time taken for insertion: {time.time() - start_insertion_time} seconds")
            else:
                print("No new data to insert.")
        except mysql.connector.Error as e:
            print(f"Error while connecting or manipulating the database: {e}")
        finally:
            # Close the database connection if it was initialized
            if db_model and db_model.conn.is_connected():
                db_model.conn.close()
    else:
        print("No data to insert.")

    print(f"Total time taken: {time.time() - start_time} seconds")

if __name__ == '__main__':
    populate_forest_table()
