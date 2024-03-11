import os
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

from api.routes import api_routes
from data_scripts.populate_ddbb_group_table import populate_grouped_table
from data_scripts.populate_ddbb_table import populate_database

#AEMET API parameters
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYXJpb2xhbGxhbmExMkBnbWFpbC5jb20iLCJqdGkiOiIyMDViNzYyNS00NGU5LTRhYTUtYWMwMi04NGE5YmRlMzhmNjIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcwNTUyODUwNSwidXNlcklkIjoiMjA1Yjc2MjUtNDRlOS00YWE1LWFjMDItODRhOWJkZTM4ZjYyIiwicm9sZSI6IiJ9.m5VUOP_qqVXBEiM5Iex2EoLYGUeaf0qfmey2EC62GeI'
# Calculate yesterday's date
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')

# Calculate the date 15 days before yesterday
start_date_dt = yesterday - timedelta(days=15)
start_date_str = start_date_dt.strftime('%Y-%m-%d')

# Construct the parameter strings
start_date = start_date_str + 'T00%3A00%3A00UTC'
end_date = yesterday_str + 'T00%3A00%3A00UTC'
station_ids = ['2462', '3111D','3266A','3110C'] 

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register the blueprint
app.register_blueprint(api_routes)

# Function to create and return a SQLite connection
def create_connection():
    return sqlite3.connect('weather_data.db')

# Check if there is data in the tables, and if not, populate the grouped table
def check_and_populate():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Execute query to get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    
    if 'weather_data' not in tables and 'grouped_weather_data' not in tables:
        print("Both weather_data and grouped_weather_data tables do not exist.")
        populate_database(api_key, start_date, end_date, station_ids)
        populate_grouped_table()
        return
    elif 'weather_data' not in tables:
        print("weather_data table does not exist.")
        populate_database(api_key, start_date, end_date, station_ids)
        return
    elif 'grouped_weather_data' not in tables:
        print("grouped_weather_data table does not exist.")
        populate_grouped_table()
        return

    cursor.execute('SELECT COUNT(*) FROM weather_data')
    weather_data_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM grouped_weather_data')
    grouped_data_count = cursor.fetchone()[0]

    if weather_data_count == 0 and grouped_data_count == 0:
        print("Both weather_data and grouped_weather_data tables are empty. Populating grouped_weather_data table.")
        populate_database(api_key, start_date, end_date, station_ids)
        populate_grouped_table()
    elif weather_data_count > 0 and grouped_data_count == 0:
        print("weather_data table has data, but grouped_weather_data table is empty.")
        populate_grouped_table()
    elif weather_data_count == 0 and grouped_data_count > 0:
        print("grouped_weather_data table has data, but weather_data table is empty.")
        populate_database(api_key, start_date, end_date, station_ids)
    else:
        print("Both weather_data and grouped_weather_data tables have data.")

    conn.close()


# Check if the data is recent
def check_recent_data():
    conn = create_connection()
    cursor = conn.cursor()

    # Get the last date from weather_data table
    cursor.execute('SELECT MAX(fecha) FROM weather_data')
    last_date_weather_data = cursor.fetchone()[0]

    # Get the last date from grouped_weather_data table
    cursor.execute('SELECT MAX(window_start) FROM grouped_weather_data')
    last_date_grouped_data = cursor.fetchone()[0]

    # Convert last_date_weather_data and last_date_grouped_data to datetime objects
    last_date_weather_data = datetime.strptime(last_date_weather_data, '%Y-%m-%d %H:%M:%S') if last_date_weather_data else None
    last_date_grouped_data = datetime.strptime(last_date_grouped_data, '%Y-%m-%d') if last_date_grouped_data else None

    # Close the connection
    conn.close()

    # Check if the last date is more than 15 days ago for either table
    if last_date_weather_data is not None and datetime.now() - last_date_weather_data > timedelta(days=2):
        print("Warning: Last weather data is more than 3 days old.")
    if last_date_grouped_data is not None and datetime.now() - last_date_grouped_data > timedelta(days=2):
        print("Warning: Last grouped data is more than 3 days old.")

if __name__ == "__main__":
    # Step 1: Check and populate grouped table if necessary
    check_and_populate()
    # Step 2: Check if data is recent
    check_recent_data()
    # Step 3: Run the API
    ## if you want to test locally:
    #app.run(debug=True)
    ## if you want to run dev on the host
    app.run(host='0.0.0.0', debug=True)