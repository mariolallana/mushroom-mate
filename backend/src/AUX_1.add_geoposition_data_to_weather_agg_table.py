import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Add new columns to the existing table
cursor.execute('ALTER TABLE weather_data_grouped ADD COLUMN latitude REAL')
cursor.execute('ALTER TABLE weather_data_grouped ADD COLUMN longitude REAL')
cursor.execute('ALTER TABLE weather_data_grouped ADD COLUMN altitude REAL')

# Commit the changes and close the connection
conn.commit()
conn.close()
