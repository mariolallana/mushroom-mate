import logging
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
from meteostat import Stations, Daily
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

# Configuration
MAX_RETRIES = 3
INITIAL_DELAY = 2
MAX_DELAY = 30
BATCH_SIZE = 100
MAX_WORKERS = 5  # Reduced from 10
RATE_LIMIT_DELAY = 1  # 1 second delay between API calls
WEATHER_DAYS = 20

def find_nearest_station(lat, lon, radius=50000):
    """Find the nearest weather station within the given radius (in meters)."""
    stations = Stations()
    nearby_stations = stations.nearby(lat, lon, radius)
    nearest_station = nearby_stations.fetch(1)
    if nearest_station.empty:
        raise ValueError(f"No station found within {radius/1000}km of coordinates ({lat}, {lon})")
    return nearest_station.iloc[0]

@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((ValueError, Exception))
)
def fetch_weather_data(lat, lon, start_date, end_date):
    """Fetch historical weather data for the given coordinates and date range."""
    try:
        station = find_nearest_station(lat, lon)
        #logging.info(f"Using station: {station['name']} (ID: {station.name}) for coordinates ({lat}, {lon})")
        
        data = Daily(station.name, start_date, end_date)
        weather_data = data.fetch()

        #if weather_data is None or weather_data.empty:
        #    raise ValueError(f"No data returned from API or data is empty for station {station['name']} and dates {start_date} to {end_date}")

        if 'prcp' in weather_data.columns:
            weather_data['prec_acc_3_days'] = weather_data['prcp'].rolling(3).sum().fillna(0)
            weather_data['prec_acc_7_days'] = weather_data['prcp'].rolling(7).sum().fillna(0)
            weather_data['prec_acc_15_days'] = weather_data['prcp'].rolling(15).sum().fillna(0)
        else:
            weather_data = pd.DataFrame(columns=['tmin', 'tmax', 'tavg', 'prcp', 'prec_acc_3_days', 'prec_acc_7_days', 'prec_acc_15_days'])
        
        time.sleep(RATE_LIMIT_DELAY)
        return weather_data
    except Exception as e:
        #logging.error(f"Error fetching weather data for ({lat}, {lon}): {e}")
        raise

def process_location(location_id, lat, lon, start_date, end_date):
    #logging.info(f"Processing location {location_id} at ({lat}, {lon})")
    weather_data = fetch_weather_data(lat, lon, start_date, end_date)
    if weather_data.empty:
        #logging.warning(f"No data returned for location {location_id}")
        return []

    weather_values = []
    for date, values in weather_data.iterrows():
        weather_id = f"{location_id}_{date.strftime('%Y-%m-%d')}"
        weather_values.append((
            weather_id,
            location_id,
            date.strftime('%Y-%m-%d'),
            values.get('tmin'),
            values.get('tmax'),
            values.get('tavg'),
            values.get('prcp'),
            values.get('prec_acc_3_days'),
            values.get('prec_acc_7_days'),
            values.get('prec_acc_15_days')
        ))
    return weather_values

def populate_weather_table():
    db_model = ForestModel(mysql_params)
    executor = None
    try:
        db_model.create_weather()
        #logging.info("Weather table created or already exists.")

        forest_locations = db_model.execute_query('SELECT location_id, centroide_lat, centroide_lng FROM forest')
        existing_weather = set(row['location_id'] for row in db_model.execute_query('SELECT DISTINCT location_id FROM weather'))
        
        new_locations = [loc for loc in forest_locations if loc['location_id'] not in existing_weather]
        #logging.info(f"New locations to process: {len(new_locations)}")

        #if not new_locations:
        #    logging.info("No new locations to process. Exiting.")
        #    return

        end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # Today at midnight
        start_date = end_date - timedelta(days=WEATHER_DAYS)

        # Process all locations in parallel
        all_weather_data = []
        executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        futures = [executor.submit(process_location, loc['location_id'], loc['centroide_lat'], loc['centroide_lng'], start_date, end_date) 
                   for loc in new_locations]
        
        for future in as_completed(futures):
            try:
                result = future.result(timeout=60)  # Increased timeout to 60 seconds
                if result:
                    all_weather_data.extend(result)
            except TimeoutError:
                logging.warning("A task timed out")
            except Exception as e:
                logging.error(f"Error processing location: {e}")

            # Insert data in batches as they complete
            if len(all_weather_data) >= BATCH_SIZE:
                db_model.insert_weather_bulk(all_weather_data[:BATCH_SIZE])
                logging.info(f"Inserted batch of {BATCH_SIZE} weather records")
                all_weather_data = all_weather_data[BATCH_SIZE:]

        # Insert any remaining data
        if all_weather_data:
            db_model.insert_weather_bulk(all_weather_data)
            logging.info(f"Inserted final batch of {len(all_weather_data)} weather records")

    except Exception as e:
        logging.error(f"Error in populate_weather_table: {e}")
    finally:
        if executor:
            executor.shutdown(wait=False)
        db_model.close()
        logging.info("Script finished.")

if __name__ == '__main__':
    populate_weather_table()