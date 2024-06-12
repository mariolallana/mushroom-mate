import numpy as np
import requests
import time
from threading import Event, Lock
import signal
import sys, os
import pandas as pd

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

# Importar la clase ForestModel y los parámetros de configuración de MySQL
from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params

# Límites aproximados de la Comunidad de Madrid en EPSG:4326
min_lat, max_lat = 40.3123, 40.9688
min_lon, max_lon = -4.2914, -3.1625

# Distancia entre puntos en grados (aproximadamente 500 metros)
lat_diff = 0.0045
lon_diff = 0.0057

# Generar la matriz de puntos
lat_points = np.arange(min_lat, max_lat, lat_diff)
lon_points = np.arange(min_lon, max_lon, lon_diff)
locations = [(lat, lon) for lat in lat_points for lon in lon_points]

# Limitar a las primeras 100 ubicaciones para pruebas
# locations = locations[:100]

# Mostrar cuántos puntos hay en total
print(f"Total points: {len(locations)}")

stop_event = Event()

def fetch_elevation(lat, lon, retries=3, delay=2):
    elevation_api_url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    for attempt in range(retries):
        if stop_event.is_set():
            return None
        try:
            response = requests.get(elevation_api_url)
            response.raise_for_status()
            elevation_data = response.json()
            if 'results' in elevation_data and len(elevation_data['results']) > 0:
                return elevation_data['results'][0]['elevation']
            else:
                return None
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                print("Too many requests, backing off...")
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                print(f"Request error: {e}, attempt {attempt + 1}")
                time.sleep(2 ** attempt)  # Exponential backoff for other errors
    return None

def get_elevations(locations, db_model):
    elevations = []
    lock = Lock()
    progress = {"count": 0, "errors": 0}
    stop_message_logged = False

    for lat, lon in locations:
        if stop_event.is_set():
            if not stop_message_logged:
                print("Stop event set, exiting get_elevations")
                stop_message_logged = True
            break
        print(f"Fetching elevation for {lat}, {lon}")
        try:
            elevation = fetch_elevation(lat, lon)
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

                # Insertar en bloques de 100 registros
                if len(elevations) >= 100:
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
    db_model.create_elevation_table()

    # Obtener las altitudes para la matriz de puntos
    progress = get_elevations(locations, db_model)
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
