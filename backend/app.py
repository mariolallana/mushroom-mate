import os
#import sqlite3
import mysql.connector
from datetime import datetime, timedelta
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

from apscheduler.schedulers.background import BackgroundScheduler
from data_scripts.weather_updater import update_weather_table
from data_scripts.update_mushroom_prob_table import update_probabilities
from data_scripts.populate_forest_table import populate_forest_table
from data_scripts.populate_mushroom_species_table import populate_mushroom_species_table

from api.routes import api_routes
from api.controllers.db_config import mysql_params 
#from backend.data_scripts.OLD.populate_ddbb_group_table import populate_grouped_table
#from backend.data_scripts.OLD.populate_ddbb_table import populate_database
#from backend.data_scripts.OLD.populate_mushroom_species import populate_species_table
#from data_scripts.populate_ddbb_forest_table import populate_forest_table

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
#CORS(app)  # Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register the blueprint
#app.register_blueprint(api_routes)
app.register_blueprint(api_routes, url_prefix='/api')

# Función para crear y devolver una conexión MySQL
def create_connection():
        return mysql.connector.connect(**mysql_params)

# Check if there is data in the tables, and if not, populate the grouped table
def check_and_populate():
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM forest')
        forest_data_count = cursor.fetchone()[0]

        if forest_data_count == 0:
            print("Forest table is empty. Populating forest table.")
            populate_forest_table()
        else:
            print("Forest table has data.")
    except mysql.connector.Error as e:
        print(f"Error checking or populating forest table: {e}")
    finally:
        if conn:
            conn.close()


# Function to start the scheduler
def start_scheduled_daily_data_update():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_weather_table, 'interval', days=1)
    scheduler.add_job(update_probabilities, 'interval', days=1)
    scheduler.start()


if __name__ == "__main__":
    # Step 1: Check and populate forest table if necessary
    check_and_populate()
    # populate species table
    populate_mushroom_species_table()
    # populate forest table
    # Start the weather update scheduler
    ###########33start_scheduled_daily_data_update()
    # update_weather_table()
    ###########33update_probabilities()
    #populate_forest_table()
    # Step 3: Run the API
    ## if you want to test locally:
    #app.run(debug=True)
    ## if you want to run dev on the host
    app.run(host='0.0.0.0', debug=True)