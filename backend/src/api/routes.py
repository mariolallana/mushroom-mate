####################################################
## 3 ## Parte de setup de back end API
####################################################

from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to create and return a SQLite connection
def create_connection():
    return sqlite3.connect('weather_data.db')

# Endpoint to get weather data
@app.route('/weather-data', methods=['GET'])
def get_weather_data():
    # Create a new SQLite connection for each request
    conn = create_connection()
    query = 'SELECT * FROM weather_data'
    result_df = pd.read_sql(query, conn)
    # Close the connection after use
    conn.close()
    return jsonify(result_df.to_dict(orient='records'))
    
# Endpoint to get location data
@app.route('/weather_data_grouped', methods=['GET'])
def get_location_data():
    query = 'SELECT * FROM weather_data_grouped '
    conn = create_connection()
    result_df = pd.read_sql(query, conn)
    conn.close()
    return jsonify(result_df.to_dict(orient='records'))


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)