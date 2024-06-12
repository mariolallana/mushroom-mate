import mysql.connector
import pandas as pd
import sys
import os
# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params 

# Función para crear y devolver una conexión MySQL

conn = mysql.connector.connect(**mysql_params)

# Query the first 5 rows from the 'weather_data' table
query = 'SELECT * FROM weather LIMIT 5'
result_df = pd.read_sql(query, conn)

# Print the DataFrame
print(result_df)

# Close the database connection
conn.close()
