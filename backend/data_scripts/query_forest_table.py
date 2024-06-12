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
forest_query = 'SELECT forest_id, tipo_id, tipo_desc, centroide_lat, centroide_lng, location_id FROM forest'
forest_locations = pd.read_sql(forest_query, conn)

print("Forest rows loaded:", forest_locations.head())  # Print the first few rows to check data
print(tabulate(forest_locations, headers='keys', tablefmt='psql'))