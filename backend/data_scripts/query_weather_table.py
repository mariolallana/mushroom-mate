import sqlite3
import pandas as pd
from tabulate import tabulate
import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel

db_path = 'forest_data.db'  

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
db_model = ForestModel(db_path)

# Get all locations from the forest table
weather_query = 'SELECT * FROM weather'
weather_locations = pd.read_sql(weather_query, conn)

print("Weather rows loaded:", weather_locations.head())  # Print the first few rows to check data
print(tabulate(weather_locations, headers='keys', tablefmt='psql'))