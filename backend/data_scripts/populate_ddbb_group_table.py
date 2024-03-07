import sys
import os
import pandas as pd
from tabulate import tabulate

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import WeatherDatabase
from data_scripts.get_location_coordinates import get_coordinates_and_altitude

def populate_grouped_table():
    # Connect to the database
    weather_db = WeatherDatabase()
    
    # weather_db.drop_grouped_weather_table()

    # Call the method to create the grouped_weather_data table
    weather_db.create_grouped_weather_data_table()

    # Query grouped data
    grouped_data = weather_db.query_grouped_data()
    #print("Structure of grouped_data:")
    #print(grouped_data.head())  # Display the first few rows to inspect the structure

    # Insert the grouped data into the grouped_weather_data table
    for index, row in grouped_data.iterrows():
        data = {
            'indicativo': row['indicativo'],
            'nombre': row['nombre'],
            'provincia': row['provincia'],
            'window_start': row['window_start'],
            'total_prec': row['total_prec'],
            'media_diaria_prec': row['media_diaria_prec'],
            'min_tmed': row['min_tmed'],
            'max_tmed': row['max_tmed'],
            'media_tmed': row['media_tmed'],
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'altitude': row['altitude']
        }
        weather_db.insert_grouped_weather_data(data)


    # Update geolocation data
    locations = weather_db.query_all_locations_gw_data()
    geo_data = get_coordinates_and_altitude(locations)
    weather_db.update_grouped_weather_data_geo(geo_data)

    # Example: Query all data from the table
    query = 'SELECT * FROM grouped_weather_data WHERE window_start = "2024-01-29"'
    result_df = pd.read_sql(query, weather_db.conn)
    print(tabulate(result_df, headers='keys', tablefmt='psql'))

    # Close the connection
    weather_db.close_connection()

