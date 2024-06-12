import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
from meteostat import Point, Daily
import sys
import os
from pyproj import Transformer
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, Event
import time
import hashlib
import pickle  # Importing pickle module

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

def create_connection():
    return mysql.connector.connect(**mysql_params)

def convert_to_wgs84(lat, lon):
    """Convert coordinates from EPSG:3395 to EPSG:4326."""
    transformer = Transformer.from_crs("epsg:3395", "epsg:4326", always_xy=True)
    lon, lat = transformer.transform(lon, lat)
    return lat, lon  # Reducing precision to 4 decimal places

def generate_weather_id(location_id, date):
    """Generate a unique weather_id based on location_id and date using MD5."""
    unique_string = f"{location_id}_{date}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def fetch_weather_data(lat, lon, start_date, end_date, retries=3):
    """Fetch historical weather data for the given coordinates and date range."""
    location = Point(lat, lon)
    data = Daily(location, start_date, end_date)

    for attempt in range(retries):
        try:
            weather_data = data.fetch()
            if weather_data is None or weather_data.empty:
                raise ValueError("No data returned from API or data is empty")

            if 'prcp' in weather_data.columns:
                weather_data['prec_acc_3_days'] = weather_data['prcp'].rolling(3).sum().fillna(0)
                weather_data['prec_acc_7_days'] = weather_data['prcp'].rolling(7).sum().fillna(0)
                weather_data['prec_acc_15_days'] = weather_data['prcp'].rolling(15).sum().fillna(0)
            else:
                weather_data = pd.DataFrame(columns=['tmin', 'tmax', 'tavg', 'prcp', 'prec_acc_3_days', 'prec_acc_7_days', 'prec_acc_15_days'])
            return weather_data
        except (EOFError, pickle.UnpicklingError, ValueError) as e:
            print(f"Error fetching weather data: {e}, attempt {attempt + 1}")
            time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            print(f"Unexpected error: {e}, attempt {attempt + 1}")
            time.sleep(2 ** attempt)  # Exponential backoff
    return pd.DataFrame(columns=['tmin', 'tmax', 'tavg', 'prcp', 'prec_acc_3_days', 'prec_acc_7_days', 'prec_acc_15_days'])

def process_location(row, start_date, end_date, stop_event):
    if stop_event.is_set():
        return

    lat, lon = row['centroide_lat'], row['centroide_lng']
    lat, lon = convert_to_wgs84(lat, lon)

    try:
        conn = create_connection()
        db_model = ForestModel(mysql_params, connection=conn)

        weather_data = fetch_weather_data(lat, lon, start_date, end_date)
        if weather_data.empty:
            print(f"No data returned for location {row['location_id']}")
            return

        for _, values in weather_data.iterrows():
            if stop_event.is_set():
                return
            weather_id = generate_weather_id(row['location_id'], values.name.strftime('%Y-%m-%d'))
            weather_values = (
                weather_id,
                row['location_id'],
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
    except mysql.connector.Error as e:
        print(f"Error inserting weather data for location {row['location_id']}: {e}")
    except Exception as e:
        print(f"Unexpected error for location {row['location_id']}: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def populate_weather_table():
    conn = create_connection()
    try:
        forest_query = 'SELECT location_id, centroide_lat, centroide_lng FROM forest'
        forest_locations = pd.read_sql(forest_query, conn)
        print("Forest locations loaded:", forest_locations.head())
    finally:
        if conn and conn.is_connected():
            conn.close()

    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)

    stop_event = Event()

    def shutdown_handler(signum, frame):
        print("Shutdown initiated...")
        stop_event.set()

    # Register the shutdown handler for graceful shutdown
    import signal
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_location, row, start_date, end_date, stop_event) for index, row in forest_locations.iterrows()]

            for future in as_completed(futures):
                if stop_event.is_set():
                    break
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in thread execution: {e}")
    except KeyboardInterrupt:
        print("Process interrupted. Shutting down...")
        stop_event.set()
        executor.shutdown(wait=False)
        sys.exit(1)

if __name__ == '__main__':
    populate_weather_table()

