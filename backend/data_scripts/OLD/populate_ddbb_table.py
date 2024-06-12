# backend/src/data_scripts/populate_ddbb_table.py

import sys
import os
import pandas as pd
from tabulate import tabulate

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

# Now 'backend' directory should be in sys.path
#print(sys.path)

from data_scripts.fetch_data import fetch_data
from api.controllers.models import WeatherDatabase  # Adjust the import path

def populate_database(api_key, start_date, end_date, station_ids):
    # Create an instance of WeatherDatabase
    weather_db = WeatherDatabase()

    # Fetch data
    data_to_insert = fetch_data(api_key, start_date, end_date, station_ids)

    # Insert the fetched data into the SQLite table
    for _, row in data_to_insert.iterrows():
        data = {
            'fecha': row['fecha'],
            'indicativo': row['indicativo'],
            'nombre': row['nombre'],
            'provincia': row['provincia'],
            'tmed': row['tmed'],
            'prec': row['prec']
        }
        weather_db.insert_weather_data(data)

    # Example: Query all data from the table
    query = 'SELECT * FROM weather_data WHERE tmed > 0'
    result_df = pd.read_sql(query, weather_db.conn)
    #print(tabulate(result_df, headers='keys', tablefmt='psql'))

    # Close the connection
    weather_db.close_connection()

