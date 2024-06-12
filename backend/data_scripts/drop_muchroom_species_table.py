import sqlite3
import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel

# Database path
DB_PATH = 'forest_data.db'  # Change to your actual database path

# Initialize the ForestModel
db_model = ForestModel(DB_PATH)

# Drop and recreate the mushroom_species table
db_model.drop_mushroom_species_table()  # Call the method to execute
print("Dropped mushroom species table")
db_model.create_mushroom_species_table()  # Call the method to execute
print("Created mushroom species table")
