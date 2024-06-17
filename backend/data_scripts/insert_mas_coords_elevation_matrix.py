import numpy as np
import requests
import time
from threading import Event, Lock
import signal
import sys, os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

# Importar la clase ForestModel y los parámetros de configuración de MySQL
from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

# Límites aproximados de la Comunidad de Madrid en EPSG:4326
min_lat, max_lat = 39.90578228589034, 41.161733975841756
min_lon, max_lon = -4.5763664094590535, -3.0709048477353535

# Distancia entre puntos en grados (aproximadamente 500 metros)
lat_diff = 0.0045
lon_diff = 0.0057

# Generar la matriz de puntos
lat_points = np.arange(min_lat, max_lat, lat_diff)
lon_points = np.arange(min_lon, max_lon, lon_diff)
locations = [(round(lat, 4), round(lon, 4)) for lat in lat_points for lon in lon_points]

# Mostrar cuántos puntos hay en total
print(f"Total points: {len(locations)}")

# Chequear los primeros registros de locations
print("Sample of locations:", locations[:5])

stop_event = Event()
cache = {}
too_many_requests_count = 0

def fetch_elevation(lat, lon, retries=3, delay=2):
    global too_many_requests_count

    if (lat, lon) in cache:
        return cache[(lat, lon)]
    
    elevation_api_url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    for attempt in range(retries):
        if stop_event.is_set():
            return None
        try:
            response = requests.get(elevation_api_url)
            response.raise_for_status()
            elevation_data = response.json()
            if 'results' in elevation_data and len(elevation_data['results']) > 0:
                elevation = elevation_data['results'][0]['elevation']
                cache[(lat, lon)] = elevation
                too_many_requests_count = 0  # Reset counter on successful request
                return elevation
            else:
                return None
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                too_many_requests_count += 1
                backoff_time = delay * (2 ** attempt)
                print(f"Too many requests, backing off for {backoff_time} seconds...")
                time.sleep(backoff_time)  # Exponential backoff
                if too_many_requests_count >= 5:  # Threshold for extended rest
                    print("Too many 'Too many requests' responses, resting for 30 seconds...")
                    time.sleep(30)  # Extended rest period
            else:
                print(f"Request error: {e}, attempt {attempt + 1}")
                time.sleep(2 ** attempt)  # Exponential backoff for other errors
    return None

def get_elevations(locations, db_model):
    elevations = []
    lock = Lock()
    progress = {"count": 0, "errors": 0}
    stop_message_logged = False

    with ThreadPoolExecutor(max_workers=10) as executor:  # Reduced number of workers
        future_to_location = {executor.submit(fetch_elevation, lat, lon): (lat, lon) for lat, lon in locations}
        for future in as_completed(future_to_location):
            lat, lon = future_to_location[future]
            if stop_event.is_set():
                if not stop_message_logged:
                    print("Stop event set, exiting get_elevations")
                    stop_message_logged = True
                break
            try:
                elevation = future.result()
                if elevation is not None:
                    elevations.append((lat, lon, elevation))
                    print(f"Elevation for {lat}, {lon}: {elevation}")
                else:
                    progress["errors"] += 1
            except Exception as e:
                print(f"Error fetching elevation for {lat}, {lon}: {e}")
                progress["errors"] += 1
            finally:
                with lock:
                    progress["count"] += 1
                    if progress["count"] % 10 == 0:
                        print(f"Processed {progress['count']} locations, Errors: {progress['errors']}")

                    # Insertar en bloques de 1000 registros
                    if len(elevations) >= 1000:
                        insert_elevations_batch(elevations, db_model)
                        elevations.clear()  # Limpiar la lista después de insertar

    # Insertar cualquier registro restante
    if elevations:
        insert_elevations_batch(elevations, db_model)

    return progress

def insert_elevations_batch(elevations, db_model):
    if elevations:
        elevation_df = pd.DataFrame(elevations, columns=['latitude', 'longitude', 'altitude'])
        db_model.insert_elevations(elevation_df.values.tolist())
        print(f"Inserted {len(elevations)} elevations")

def populate_elevation_table():
    # Crear la conexión a la base de datos y la tabla
    db_model = ForestModel(mysql_params)

    # Obtener las coordenadas ya presentes en la tabla
    existing_locations = db_model.get_existing_elevation_coordinates()
    existing_locations_set = set((round(lat, 4), round(lon, 4)) for lat, lon in existing_locations)  # Convertir a set para comparación eficiente

    print(f"Existing points: {len(existing_locations_set)}")

    # Chequear los primeros registros de existing_locations_set
    print("Sample of existing locations:", list(existing_locations_set)[:5])

    # Filtrar las ubicaciones para obtener solo las que faltan
    missing_locations = [(lat, lon) for lat, lon in locations if (lat, lon) not in existing_locations_set]
    print(f"Missing points: {len(missing_locations)}")

    # Chequear los primeros registros de missing_locations
    print("Sample of missing locations:", missing_locations[:5])

    # Obtener las altitudes para la matriz de puntos faltantes
    progress = get_elevations(missing_locations, db_model)
    print(f"Total elevations fetched: {progress['count']}, Errors: {progress['errors']}")

    print("Elevation data insertion completed.")

def shutdown_handler(signum, frame):
    print("Shutdown initiated...")
    stop_event.set()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    start_time = time.time()
    try:
        populate_elevation_table()
    except KeyboardInterrupt:
        print("Process interrupted. Shutting down...")
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")
