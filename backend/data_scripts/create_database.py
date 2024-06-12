import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel

# Database path
DB_PATH = 'forest_data.db'  # Change to your actual database path

def create_database():
    # Initialize the database model
    db_model = ForestModel(DB_PATH)
    # Create tables
    db_model.create_tables()
    print("Database and tables created successfully.")

if __name__ == '__main__':
    create_database()
