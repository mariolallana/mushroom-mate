#import sqlite3
import mysql.connector
import pandas as pd
from datetime import datetime
import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from data_scripts.mushroom_probability_calculation import calculate_probabilities

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params 


# Database path
#DB_PATH = 'forest_data.db'

def get_connection():
    return mysql.connector.connect(**mysql_params)

def fetch_locations():
    conn = get_connection()
    query = '''
        SELECT location_id
        FROM forest
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    return df['location_id'].astype(str).tolist()

def fetch_mushroom_species():
    conn = get_connection()
    query = '''
        SELECT specie_id, specie_name
        FROM mushroom_species
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    mushroom_list = df.to_dict('records')  # Convert DataFrame to a list of dictionaries
    print("Fetched mushroom species:", mushroom_list)  # Debugging output
    return mushroom_list


def update_probabilities():
    conn = get_connection()
    locations = fetch_locations()
    mushrooms = fetch_mushroom_species()

    db_model = ForestModel(mysql_params)
    db_model.drop_mushroom_probability_table()
    db_model.create_mushroom_probability()

    for location_id in locations:
        probabilities = calculate_probabilities(location_id)
        if probabilities:
            for probability_info in probabilities:
                if isinstance(probability_info, dict):
                    if 'error' in probability_info:
                        print(f"Error for location {location_id}: {probability_info['error']}")
                        continue  

                    specie_id = next((m['specie_id'] for m in mushrooms if m['specie_name'] == probability_info.get('specie_name')), None)
                    if specie_id:
                        db_model.update_probability_record(location_id, specie_id, probability_info.get('probability'))
                else:
                    print(f"Unexpected data format: {probability_info}")    

    conn.close()
    print("Mushroom prob table update completed.")



def print_first_ten_probabilities():
    conn = get_connection()
    query = '''
        SELECT * FROM mushroom_probabilities
        ORDER BY last_updated DESC
        LIMIT 10
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    print("First 10 entries in mushroom_probabilities:")
    print(df)


if __name__ == '__main__':
    update_probabilities()
    print_first_ten_probabilities()
