import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
from meteostat import Point, Daily
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event, Lock
import time
import pickle  # Importar el módulo pickle
import signal

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

def create_connection():
    return mysql.connector.connect(**mysql_params)

def generate_weather_id(location_id, date):
    """Generate a unique weather_id based on location_id and date."""
    return f"{location_id}_{date}"

def fetch_weather_data(lat, lon, start_date, end_date, retries=3, delay=2):
    """Fetch historical weather data for the given coordinates and date range."""
    location = Point(lat, lon)
    data = Daily(location, start_date, end_date)

    for attempt in range(retries):
        try:
            weather_data = data.fetch()
            if weather_data is None or weather_data.empty:
                raise ValueError(f"No data returned from API or data is empty for coordinates ({lat}, {lon}) and dates {start_date} to {end_date}")

            if 'prcp' in weather_data.columns:
                weather_data['prec_acc_3_days'] = weather_data['prcp'].rolling(3).sum().fillna(0)
                weather_data['prec_acc_7_days'] = weather_data['prcp'].rolling(7).sum().fillna(0)
                weather_data['prec_acc_15_days'] = weather_data['prcp'].rolling(15).sum().fillna(0)
            else:
                weather_data = pd.DataFrame(columns=['tmin', 'tmax', 'tavg', 'prcp', 'prec_acc_3_days', 'prec_acc_7_days', 'prec_acc_15_days'])
            return weather_data
        except (EOFError, pickle.UnpicklingError, ValueError) as e:
            print(f"Error fetching weather data: {e}, attempt {attempt + 1}")
            time.sleep(delay * (2 ** attempt))  # Exponential backoff
        except Exception as e:
            print(f"Unexpected error: {e}, attempt {attempt + 1}")
            time.sleep(delay * (2 ** attempt))  # Exponential backoff
    return pd.DataFrame(columns=['tmin', 'tmax', 'tavg', 'prcp', 'prec_acc_3_days', 'prec_acc_7_days', 'prec_acc_15_days'])

def fetch_weather_data_with_fallback(lat, lon, start_date, end_date, max_distance=0.5, step=0.02):
    """Fetch historical weather data for the given coordinates and date range with fallback to nearby coordinates."""
    offsets = [-step, 0, step]
    for distance in range(1, int(max_distance / step) + 1):
        for dlat in offsets:
            for dlon in offsets:
                if dlat == 0 and dlon == 0:
                    continue
                try:
                    weather_data = fetch_weather_data(lat + dlat * distance, lon + dlon * distance, start_date, end_date)
                    if not weather_data.empty:
                        print(f"Found data for coordinates ({lat + dlat * distance}, {lon + dlon * distance})")
                        return weather_data
                except ValueError as e:
                    print(e)
    print(f"No data found for ({lat}, {lon}) within {max_distance} degrees range.")
    return pd.DataFrame(columns=['tmin', 'tmax', 'tavg', 'prcp', 'prec_acc_3_days', 'prec_acc_7_days', 'prec_acc_15_days'])

def process_location(row, start_date, end_date, stop_event, results, lock, unique_keys):
    if stop_event.is_set():
        return

    lat, lon = row['centroide_lat'], row['centroide_lng']
    location_id = row['location_id']

    print(f"Fetching weather data for coordinates ({lat}, {lon}) and dates {start_date} to {end_date}")
    weather_data = fetch_weather_data_with_fallback(lat, lon, start_date, end_date)
    if weather_data.empty:
        print(f"No data returned for location {location_id}")
        return

    for _, values in weather_data.iterrows():
        if stop_event.is_set():
            return
        weather_id = generate_weather_id(location_id, values.name.strftime('%Y-%m-%d'))
        
        with lock:
            if weather_id in unique_keys:
                continue
            unique_keys.add(weather_id)
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
            results.append(weather_values)
            if len(results) >= 100:
                insert_weather_data_batch(results)

def insert_weather_data_batch(results):
    conn = create_connection()
    db_model = ForestModel(mysql_params, connection=conn)
    try:
        if results:
            db_model.insert_weather_bulk(results)
            print(f"Inserted {len(results)} records into the weather table")
            results.clear()
    except mysql.connector.Error as e:
        conn.rollback()
        if e.errno == 1062:
            print(f"Duplicate entry error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def drop_and_create_weather_table():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS weather')
        conn.commit()
        print("Dropped existing weather table.")
    except mysql.connector.Error as e:
        print(f"Error dropping weather table: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

    conn = create_connection()
    try:
        db_model = ForestModel(mysql_params, connection=conn)
        db_model.create_weather()
        print("Created new weather table.")
    except mysql.connector.Error as e:
        print(f"Error creating weather table: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def populate_weather_table():
    # drop_and_create_weather_table()  # Drop and recreate the weather table at the beginning (commented out)

    conn = create_connection()
    try:
        forest_query = 'SELECT location_id, centroide_lat, centroide_lng FROM forest'
        forest_locations = pd.read_sql(forest_query, conn)
        print("Forest locations loaded:", forest_locations.head())
        
        weather_query = 'SELECT DISTINCT location_id FROM weather'
        existing_weather = pd.read_sql(weather_query, conn)
        existing_weather_set = set(existing_weather['location_id'])
        print(f"Existing weather records: {len(existing_weather_set)}")

        new_locations = forest_locations[~forest_locations['location_id'].isin(existing_weather_set)]
        print(f"New locations to process: {len(new_locations)}")
    finally:
        if conn and conn.is_connected():
            conn.close()

    end_date = datetime.today()
    start_date = end_date - timedelta(days=20)

    stop_event = Event()

    def shutdown_handler(signum, frame):
        print("Shutdown initiated...")
        stop_event.set()
        raise KeyboardInterrupt

    # Register the shutdown handler for graceful shutdown
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    results = []
    unique_keys = set()
    lock = Lock()

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_location, row, start_date, end_date, stop_event, results, lock, unique_keys) for index, row in new_locations.iterrows()]

            for future in as_completed(futures):
                if stop_event.is_set():
                    break
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in thread execution: {e}")

        insert_weather_data_batch(results)
    except KeyboardInterrupt:
        print("Process interrupted. Shutting down...")
        stop_event.set()
        insert_weather_data_batch(results)
        sys.exit(1)

if __name__ == '__main__':
    populate_weather_table()
