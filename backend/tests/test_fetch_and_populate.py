import sys
import os
import pandas as pd
from tabulate import tabulate

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

# backend/src/data_scripts/test_fetch_and_populate.py
from data_scripts.fetch_data import fetch_data
from data_scripts.populate_ddbb_table import populate_database
from data_scripts.populate_ddbb_group_table import populate_grouped_table
from api.controllers.models import WeatherDatabase

def main():
    # Replace 'YOUR_API_KEY', 'START_DATE', 'END_DATE', and 'STATION_IDS' with your actual values
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYXJpb2xhbGxhbmExMkBnbWFpbC5jb20iLCJqdGkiOiIyMDViNzYyNS00NGU5LTRhYTUtYWMwMi04NGE5YmRlMzhmNjIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcwNTUyODUwNSwidXNlcklkIjoiMjA1Yjc2MjUtNDRlOS00YWE1LWFjMDItODRhOWJkZTM4ZjYyIiwicm9sZSI6IiJ9.m5VUOP_qqVXBEiM5Iex2EoLYGUeaf0qfmey2EC62GeI'
    start_date = '2024-01-01T00%3A00%3A00UTC'
    end_date = '2024-01-15T00%3A00%3A00UTC'
    station_ids = ['2462', '3111D','3266A','3110C'] 

    # Fetch data and populate the database
    populate_database(api_key, start_date, end_date, station_ids)
    populate_grouped_table()

    # Query the populated data
    weather_db = WeatherDatabase()
    query = 'SELECT * FROM grouped_weather_data'
    result_df = pd.read_sql(query, weather_db.conn)
    print(tabulate(result_df, headers='keys', tablefmt='psql'))
    weather_db.close_connection()

if __name__ == "__main__":
    main()
