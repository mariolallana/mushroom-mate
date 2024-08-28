import logging
import pandas as pd
from datetime import datetime, timedelta
from meteostat import Stations, Daily
import sys
import os
import time
from math import radians, cos

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(backend_dir)

from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

# Configuration
MAX_RETRIES = 3
BATCH_SIZE = 100
RATE_LIMIT_DELAY = 1  # 1 second delay between API calls

def find_nearest_station(lat, lon):
    logging.info(f"Finding nearest station for coordinates ({lat}, {lon})")
    stations = Stations()
    nearby_stations = stations.nearby(lat, lon)
    if nearby_stations.count() == 0:
        raise ValueError(f"No station found near coordinates ({lat}, {lon})")
    nearest = nearby_stations.fetch(1)
    logging.info(f"Nearest station found: {nearest.index[0]}")
    return nearest

def get_required_stations(db_model):
    query = '''
    SELECT MIN(centroide_lat) as min_lat, MAX(centroide_lat) as max_lat,
           MIN(centroide_lng) as min_lng, MAX(centroide_lng) as max_lng
    FROM forest
    '''
    bounds = db_model.execute_query(query)[0]
    logging.info(f"Bounding box: {bounds}")
    
    # Extend the bounding box by approximately 100km in each direction
    lat_extension = 100 / 111
    lng_extension = 100 / (111 * cos(radians((bounds['min_lat'] + bounds['max_lat']) / 2)))
    
    extended_bounds = {
        'min_lat': bounds['min_lat'] - lat_extension,
        'max_lat': bounds['max_lat'] + lat_extension,
        'min_lng': bounds['min_lng'] - lng_extension,
        'max_lng': bounds['max_lng'] + lng_extension
    }
    
    logging.info(f"Extended bounding box: {extended_bounds}")
    
    stations = []
    for lat, lng in [
        (extended_bounds['min_lat'], extended_bounds['min_lng']),
        (extended_bounds['min_lat'], extended_bounds['max_lng']),
        (extended_bounds['max_lat'], extended_bounds['min_lng']),
        (extended_bounds['max_lat'], extended_bounds['max_lng'])
    ]:
        try:
            station = find_nearest_station(lat, lng)
            if not station.empty:
                stations.append({
                    'id': station.index[0],
                    'latitude': station['latitude'].values[0],
                    'longitude': station['longitude'].values[0]
                })
        except ValueError as e:
            logging.warning(f"No station found near ({lat}, {lng}): {e}")
    
    # Add stations within the original bounding box
    stations_within = Stations().bounds((bounds['min_lat'], bounds['min_lng']), 
                                        (bounds['max_lat'], bounds['max_lng']))
    stations_df = stations_within.fetch()
    for _, row in stations_df.iterrows():
        stations.append({
            'id': row.name,
            'latitude': row['latitude'],
            'longitude': row['longitude']
        })
    
    logging.info(f"Required stations: {stations}")
    return stations

def fetch_weather_data(station_id, start_date, end_date):
    """Fetch historical weather data for the given station and date range."""
    try:
        logging.info(f"Fetching weather data for station {station_id} from {start_date} to {end_date}")
        data = Daily(station_id, start_date, end_date)
        weather_data = data.fetch()

        logging.info(f"Fetched {len(weather_data)} records for station {station_id}")

        if not weather_data.empty and 'prcp' in weather_data.columns:
            weather_data['prec_acc_3_days'] = weather_data['prcp'].rolling(3).sum().fillna(0)
            weather_data['prec_acc_7_days'] = weather_data['prcp'].rolling(7).sum().fillna(0)
            weather_data['prec_acc_15_days'] = weather_data['prcp'].rolling(15).sum().fillna(0)
        else:
            logging.warning(f"No precipitation data found for station {station_id}")
            weather_data = pd.DataFrame(columns=['tmin', 'tmax', 'tavg', 'prcp', 'prec_acc_3_days', 'prec_acc_7_days', 'prec_acc_15_days'])
        
        time.sleep(RATE_LIMIT_DELAY)
        return weather_data
    except Exception as e:
        logging.error(f"Error fetching weather data for station {station_id}: {e}")
        raise

def update_weather_table():
    db_model = ForestModel(mysql_params)
    try:
        last_date = db_model.execute_query('SELECT MAX(date) as last_date FROM weather')[0]['last_date']
        if not last_date:
            logging.error("No existing weather data found. Please run populate_weather_table.py first.")
            return

        start_date = last_date + timedelta(days=1)
        end_date = datetime.now().date()

        if start_date >= end_date:
            logging.info("Weather data is up to date. No new data to fetch.")
            return

        logging.info(f"Updating weather data from {start_date} to {end_date}")

        stations = get_required_stations(db_model)
        logging.info(f"Fetching data for {len(stations)} stations: {stations}")

        all_weather_data = {}
        for station in stations:
            station_id = station['id']
            if isinstance(station_id, str) and station_id.isdigit():
                all_weather_data[station_id] = fetch_weather_data(station_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

        logging.info(f"Fetched weather data for all stations. Total records: {sum(len(data) for data in all_weather_data.values())}")

        forest_locations = db_model.execute_query('SELECT DISTINCT w.location_id, f.centroide_lat, f.centroide_lng FROM weather w JOIN forest f ON w.location_id = f.location_id')
        logging.info(f"Processing {len(forest_locations)} forest locations")

        weather_values = []
        for loc in forest_locations:
            nearest_station = min(stations, key=lambda s: (float(s['latitude']) - loc['centroide_lat'])**2 + (float(s['longitude']) - loc['centroide_lng'])**2)
            station_id = nearest_station['id']
            if station_id in all_weather_data:
                station_data = all_weather_data[station_id]
            else:
                logging.warning(f"No weather data found for station {station_id}. Skipping this location.")
                continue
            
            for date, values in station_data.iterrows():
                weather_id = f"{loc['location_id']}_{date.strftime('%Y-%m-%d')}"
                weather_values.append((
                    weather_id,
                    loc['location_id'],
                    date.strftime('%Y-%m-%d'),
                    None if pd.isna(values.get('tmin')) else values.get('tmin'),
                    None if pd.isna(values.get('tmax')) else values.get('tmax'),
                    None if pd.isna(values.get('tavg')) else values.get('tavg'),
                    None if pd.isna(values.get('prcp')) else values.get('prcp'),
                    None if pd.isna(values.get('prec_acc_3_days')) else values.get('prec_acc_3_days'),
                    None if pd.isna(values.get('prec_acc_7_days')) else values.get('prec_acc_7_days'),
                    None if pd.isna(values.get('prec_acc_15_days')) else values.get('prec_acc_15_days')
                ))

            if len(weather_values) >= BATCH_SIZE:
                db_model.insert_weather_bulk(weather_values[:BATCH_SIZE])
                logging.info(f"Inserted batch of {BATCH_SIZE} weather records")
                weather_values = weather_values[BATCH_SIZE:]

        if weather_values:
            db_model.insert_weather_bulk(weather_values)
            logging.info(f"Inserted final batch of {len(weather_values)} weather records")

    except Exception as e:
        logging.error(f"Error in update_weather_table: {e}", exc_info=True)
    finally:
        db_model.close()
        logging.info("Weather update script finished.")

if __name__ == '__main__':
    update_weather_table()