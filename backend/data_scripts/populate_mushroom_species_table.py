#import sqlite3
import mysql.connector
import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params 

# Database path
#DB_PATH = 'forest_data.db'  # Change to your actual database path

# Dummy data for mushroom_species
mushroom_data = [
    (1, 'Boletus edulis', 'A popular edible mushroom.', 21, 25.0, 5.0, 10, 30, 2000, 1500, 1200),
    (2, 'Niscalo', 'A widely collected mushroom.', 21, 20.0, 0.0, 20, 40, 1600, 1200, 1000),
    (3, 'Amanita cesarea', 'Known as Caesar\'s mushroom.', 1, 30.0, 10.0, 30, 60, 1800, 1400, 1000),
    (4, 'Cantarellus tibarius', 'Lorem ipsum lorem ipsum', 24, 30.0, 10.0, 30, 60, 1800, 1400, 1000),
    (5, 'Amanita muscaria', 'Lorem ipsum lorem ipsum', 24, 30.0, 10.0, 30, 60, 1800, 1400, 1000),
]

def populate_mushroom_species_table():
    # Connect to the SQLite database
    db_model = ForestModel(mysql_params)

    # Drop the existing mushroom_species table
    db_model.drop_mushroom_species_table()
    print("Dropped existing mushroom_species table.")

    # Recreate the mushroom_species table
    db_model.create_mushroom_species_table()
    print("Recreated mushroom_species table.")

    # Insert dummy data into the mushroom_species table
    for specie in mushroom_data:
        try:
            db_model.insert_mushroom_species(specie)
            #print(f"Inserted mushroom species: {specie[1]}")
        except mysql.connector.IntegrityError as e:
            print(f"Failed to insert {specie[1]} due to a UNIQUE constraint failure: {e}")

    # Close the database connection
    db_model.conn.close()
    print("Database connection closed.")

if __name__ == '__main__':
    populate_mushroom_species_table()
