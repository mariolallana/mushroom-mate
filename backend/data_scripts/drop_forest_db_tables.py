import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel

# Database path
DB_PATH = 'forest_data.db'  # Change to your actual database path

def drop_database():
    # Initialize the database model
    db_model = ForestModel(DB_PATH)
    # Create tables
    db_model.drop_all_tables()
    print("Database and tables created successfully.")
    db_model.close()

if __name__ == '__main__':
    drop_database()
