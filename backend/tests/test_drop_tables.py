import sqlite3
import pandas as pd
import sys
import os 

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import WeatherDatabase

def main():
    # Connect to the database
    weather_db = WeatherDatabase()
    weather_db.drop_weather_table()
    weather_db.drop_weather_table()

if __name__ == "__main__":
    main()
