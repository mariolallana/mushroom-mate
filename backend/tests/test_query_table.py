import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')

# Query the first 5 rows from the 'weather_data' table
query = 'SELECT * FROM weather_data LIMIT 5'
result_df = pd.read_sql(query, conn)

# Print the DataFrame
print(result_df)

# Close the database connection
conn.close()
