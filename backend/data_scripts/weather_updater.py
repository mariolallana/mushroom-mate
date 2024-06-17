import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
from meteostat import Point, Daily
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params 

def get_next_weather_id(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(weather_id) FROM weather')
    result = cursor.fetchone()
    return (int(result[0]) if result[0] else 0) + 1

def fetch_weather_data(lat, lon, start_date, end_date):
    """Fetch historical weather data for the given coordinates and date range."""
    logging.info(f"Fetching weather data for coordinates ({lat}, {lon}) from {start_date} to {end_date}.")
    
    # Ensure lat and lon are floats
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        logging.error("Latitude and longitude must be numeric values.")
        return pd.DataFrame()  # Return an empty DataFrame if lat and lon are not numeric
    
    # Check lat and lon ranges
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        logging.error("Latitude must be between -90 and 90, and longitude between -180 and 180.")
        return pd.DataFrame()  # Return an empty DataFrame if lat and lon are out of range

    location = Point(lat, lon)
    data = Daily(location, start_date, end_date)
    weather_data = data.fetch()

    if not weather_data.empty and 'prcp' in weather_data.columns:
        weather_data['prec_acc_3_days'] = weather_data['prcp'].rolling(3).sum().fillna(0)
        weather_data['prec_acc_7_days'] = weather_data['prcp'].rolling(7).sum().fillna(0)
        weather_data['prec_acc_15_days'] = weather_data['prcp'].rolling(15).sum().fillna(0)
        logging.info(f"Fetched {len(weather_data)} records of weather data.")
    else:
        weather_data = pd.DataFrame(columns=['tmin', 'tmax', 'tavg', 'prcp', 'prec_acc_3_days', 'prec_acc_7_days', 'prec_acc_15_days'])
        logging.warning(f"No weather data available for coordinates ({lat}, {lon}). Empty DataFrame returned.")

    return weather_data

def get_last_inserted_date(conn):
    """Fetch the latest date from the weather table."""
    logging.info("Retrieving the last inserted weather data date.")
    query = 'SELECT MAX(date) FROM weather'
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    last_date = result[0] if result[0] else None
    logging.info(f"Last inserted weather data date: {last_date}.")
    return last_date

def update_weather_table():
    logging.info("Starting weather table update.")
    conn = mysql.connector.connect(**mysql_params)
    db_model = ForestModel(mysql_params)

    last_inserted_date = get_last_inserted_date(conn)
    start_date = datetime.strptime(last_inserted_date.strftime('%Y-%m-%d'), '%Y-%m-%d') + timedelta(days=1) if last_inserted_date else datetime.today() - timedelta(days=15)
    end_date = datetime.today()

    logging.info(f"Updating weather data from {start_date} to {end_date}.")
    forest_query = 'SELECT location_id, centroide_lat, centroide_lng FROM forest'
    forest_locations = pd.read_sql(forest_query, conn)

    logging.info(f"Found {len(forest_locations)} forest locations for weather data updates.")
    for index, row in forest_locations.iterrows():
        lat, lon = row['centroide_lat'], row['centroide_lng']
        location_id = row['location_id']
        logging.info(f"Processing location {location_id} at coordinates ({lat}, {lon}).")
        weather_data = fetch_weather_data(lat, lon, start_date, end_date)

        if not weather_data.empty:
            weather_id = get_next_weather_id(conn)  # Retrieve the next weather_id
            for _, values in weather_data.iterrows():
                weather_values = (
                    weather_id,
                    location_id,
                    values.name.strftime('%Y-%m-%d'),
                    values['tmin'],
                    values['tmax'],
                    values['tavg'],
                    values['prcp'],
                    values['prec_acc_3_days'],
                    values['prec_acc_7_days'],
                    values['prec_acc_15_days'],
                )
                db_model.insert_weather(weather_values)
                logging.info(f"Inserted weather data for location {location_id} on {values.name.strftime('%Y-%m-%d')}.")
                weather_id += 1
        else:
            logging.warning(f"No weather data inserted for location {location_id} due to lack of data.")

    conn.close()
    logging.info("Weather table update completed.")

if __name__ == '__main__':
    update_weather_table()
