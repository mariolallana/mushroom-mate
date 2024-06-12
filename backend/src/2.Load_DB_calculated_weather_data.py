import pandas as pd
from tabulate import tabulate
import sqlite3

# Create a SQLite connection
conn = sqlite3.connect('weather_data.db')

# Query data from the SQLite database
query = """
    SELECT indicativo, nombre, provincia,
           SUM(prec) as total_prec,
           AVG(prec) as media_diaria_prec,
           MIN(tmed) as min_tmed,
           MAX(tmed) as max_tmed,
           AVG(tmed) as media_tmed,
           0.0 as latitude,
           0.0 as longitude,
           0.0 as  altitude
    FROM original_weather_data
    GROUP BY indicativo, nombre, provincia
"""

# Fetch data into a DataFrame
df_grouped = pd.read_sql_query(query, conn)

# Close the SQLite connection
conn.close()

# Print the transformed data in a tabular format
print("Transformed Data:")
print(tabulate(df_grouped, headers='keys', tablefmt='pretty'))

# Create a new SQLite connection
conn = sqlite3.connect('weather_data.db')

# Insert df_grouped data into another table in the SQLite database
df_grouped.to_sql('weather_data_grouped', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("\nData inserted into 'weather_data_grouped' table.")
