import time
import mysql.connector
import hashlib
import sys
import os
import pandas as pd
from scipy.spatial import cKDTree
from tqdm import tqdm  # Import tqdm
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params


def fetch_elevations_from_db(db_model, chunk_size=100000):
    """Fetch elevation data from the database in chunks."""
    query = "SELECT latitude, longitude, altitude FROM elevation_data"
    offset = 0
    while True:
        chunk_query = f"{query} LIMIT {chunk_size} OFFSET {offset}"
        chunk = pd.DataFrame(db_model.execute_query(chunk_query), columns=['latitude', 'longitude', 'altitude'])
        if chunk.empty:
            break
        yield chunk
        offset += chunk_size

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
        logging.info(f"Fetched {len(aux_data)} records from the auxiliary table.")

        if not aux_data.empty:
            locations = aux_data[['centroide_lat_wgs84', 'centroide_lng_wgs84']].values
            aux_data['altitude'] = 0  # Initialize altitude column

            for elevation_chunk in fetch_elevations_from_db(db_model):
                chunk_locations = elevation_chunk[['latitude', 'longitude']].values
                chunk_altitudes = assign_elevation_to_locations(locations, elevation_chunk)
                aux_data.loc[aux_data['altitude'] == 0, 'altitude'] = chunk_altitudes

            logging.info("Elevation assignment completed.")

            # Filter out rows where 'altitude' is less than 800m
            aux_data = aux_data[aux_data['altitude'] > 800]
            logging.info(f"{len(aux_data)} records remain after altitude filtering.")

            if not aux_data.empty:
                data_tuples = [
                    (
                        row['location_id'],
                        row['tipo_id'],
                        row['tipo_desc'],
                        row['centroide_lat_wgs84'],
                        row['centroide_lng_wgs84'],
                        row['polygon'],
                        row['altitude'],
                    )
                    for _, row in aux_data.iterrows() if row['polygon'] is not None
                ]

                logging.info(f"Sample data tuple: {data_tuples[0] if data_tuples else 'No data'}")
                logging.info(f"Number of fields in data tuple: {len(data_tuples[0]) if data_tuples else 0}")

                for batch_start in tqdm(range(0, len(data_tuples), 100), desc='Inserting data', unit='batch'):
                    batch = data_tuples[batch_start:batch_start + 100]
                    db_model.insert_forest_bulk(batch, batch_size=100)  # Adjust the batch size as necessary

                logging.info("Data inserted successfully.")
            else:
                logging.warning("No data to insert after altitude filtering.")
        else:
            logging.warning("No data to insert from auxiliary table.")
    except mysql.connector.Error as e:
        logging.error(f"Error while connecting or manipulating the database: {e}")
    finally:
        # Close the database connection if it was initialized
        if db_model and db_model.conn.is_connected():
            db_model.conn.close()

    logging.info(f"Total time taken: {time.time() - start_time} seconds")

if __name__ == '__main__':
    populate_forest_table()