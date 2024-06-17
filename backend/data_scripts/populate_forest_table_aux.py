import time
import mysql.connector
import geopandas as gpd
import pandas as pd
import numpy as np
import sys
import os
from shapely.geometry import Polygon

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

# Usa un CRS proyectado para el cálculo del centroide
PROJ_CRS = 'EPSG:3395'  # Un CRS proyectado mundial como Mercator

def prepare_and_load_aux_data(file_path):
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
    gdf = gdf.to_crs('epsg:4326')  # Convertir a WGS84
    gdf['centroide_lat_wgs84'] = gdf.centroid.y
    gdf['centroide_lng_wgs84'] = gdf.centroid.x
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

    # Create a connection to the database
    db_model = ForestModel(mysql_params)

    # Create the auxiliary table
    db_model.create_forest_aux()

    # Insert data into the auxiliary table
    try:
        data_tuples = []
        for _, row in gdf.iterrows():
            if row['polygon'] is not None:
                data_tuples.append((
                    row['tipo_id'],
                    row['tipo_desc'],
                    row['centroide_lat_wgs84'],
                    row['centroide_lng_wgs84'],
                    row['polygon'],  # Assuming this is already in WKT
                    row['location_id']
                ))
        print(f"Total records to be inserted: {len(data_tuples)}")
        db_model.insert_forest_aux_bulk(data_tuples, batch_size=100)  # Ajusta el tamaño del lote según sea necesario
        print("Datos insertados en la tabla auxiliar correctamente.")
    except mysql.connector.Error as e:
        print(f"Error while connecting or manipulating the database: {e}")
    finally:
        # Close the database connection if it was initialized
        if db_model and db_model.conn.is_connected():
            db_model.conn.close()

    print(f"Total time taken for data preparation and auxiliary table insertion: {time.time() - start_time} seconds")

if __name__ == '__main__':
    file_path = r'C:\Users\mario\Downloads\mfe_madrid\MFE_30.shp'
    prepare_and_load_aux_data(file_path)
