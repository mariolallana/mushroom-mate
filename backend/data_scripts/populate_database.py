# populate_database.py

import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)


from populate_forest_table import populate_forest_table
from populate_weather_table import populate_weather_table
from populate_mushroom_species_table import populate_mushroom_species_table

def main():
    print("Populating forest table...")
    populate_forest_table()
    
    print("Populating weather table...")
    populate_weather_table()
    
    print("Populating mushroom species table...")
    populate_mushroom_species_table()
    
    print("All tables populated successfully.")

if __name__ == '__main__':
    main()
