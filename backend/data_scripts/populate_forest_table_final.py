import time
import mysql.connector
import hashlib
import sys
import os
import pandas as pd
from scipy.spatial import cKDTree

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

def generate_forest_id(location_id):
    """Generate a unique weather_id based on location_id and date using MD5."""
    unique_string = f"{location_id}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def fetch_elevations_from_db(db_model):
    """Fetch all elevation data from the database."""
    query = "SELECT latitude, longitude, altitude FROM elevation_data"
    result = db_model.execute_query(query)
    return pd.DataFrame(result, columns=['latitude', 'longitude', 'altitude'])

def assign_elevation_to_locations(locations, elevation_data):
    """Assign the nearest elevation to each location using KDTree for fast lookup."""
    tree = cKDTree(elevation_data[['latitude', 'longitude']].values)
    distances, indices = tree.query(locations)
    return elevation_data['altitude'].iloc[indices].values

def populate_forest_table():
    start_time = time.time()

    try:
        # Initialize the model with the path to the database
        db_model = ForestModel(mysql_params)
            # Create the auxiliary table
        db_model.create_forest()

        # Fetch data from the auxiliary table
        aux_data = db_model.fetch_aux_data()

        print(f"Fetched {len(aux_data)} records from the auxiliary table.")

        if not aux_data.empty:
            # Fetch all elevation data from the database
            elevation_data = fetch_elevations_from_db(db_model)
            print(f"Fetched {len(elevation_data)} records from the elevation_data table.")

            # Assign elevations to centroids
            start_elevation_time = time.time()
            locations = aux_data[['centroide_lat_wgs84', 'centroide_lng_wgs84']].values
            aux_data['altitude'] = assign_elevation_to_locations(locations, elevation_data)
            print("Asignación de datos de elevación realizada.")
            print(f"Time taken for elevation assignment: {time.time() - start_elevation_time} seconds")

            # Filter out rows where 'altitude' is less than 2000
            aux_data = aux_data[aux_data['altitude'] > 800]

            if not aux_data.empty:
                start_insertion_time = time.time()
                data_tuples = [
                    (
                        generate_forest_id(row['location_id']),
                        row['tipo_id'],
                        row['tipo_desc'],
                        row['centroide_lat_wgs84'],
                        row['centroide_lng_wgs84'],
                        row['polygon'],  # Assuming this is already in WKT
                        row['altitude'],
                        row['location_id']
                    )
                    for _, row in aux_data.iterrows() if row['polygon'] is not None
                ]
                db_model.insert_forest_bulk(data_tuples, batch_size=100)  # Ajusta el tamaño del lote según sea necesario
                print("Data inserted successfully.")
                print(f"Time taken for insertion: {time.time() - start_insertion_time} seconds")
            else:
                print("No data to insert after altitude filtering.")
        else:
            print("No data to insert from auxiliary table.")
    except mysql.connector.Error as e:
        print(f"Error while connecting or manipulating the database: {e}")
    finally:
        # Close the database connection if it was initialized
        if db_model and db_model.conn.is_connected():
            db_model.conn.close()

    print(f"Total time taken: {time.time() - start_time} seconds")

if __name__ == '__main__':
    populate_forest_table()
