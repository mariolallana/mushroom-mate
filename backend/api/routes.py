from flask import Blueprint, jsonify, request
# import sqlite3
import mysql.connector
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime, timedelta

api_routes = Blueprint('api_routes', __name__, url_prefix='/api')

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

#from api.controllers.models import WeatherDatabase
from api.controllers.models import ForestModel
from api.controllers.db_config import mysql_params 

# Function to create and return a SQLite connection

def create_connection_forest():
    return mysql.connector.connect(**mysql_params)

# Endpoint to get weather data
@api_routes.route('/weather-data', methods=['GET'])
def get_weather_data():
    # Create a new SQLite connection for each request
    conn = create_connection_forest()
    query = 'SELECT * FROM weather_data'
    result_df = pd.read_sql(query, conn)
    # Close the connection after use
    conn.close()
    return jsonify(result_df.to_dict(orient='records'))

# Endpoint to get weather data
@api_routes.route('/weather-data-group-hist', methods=['GET'])
def get_weather_group_hist_data():
    # Create a new SQLite connection for each request
    conn = create_connection_forest()
    query = 'SELECT * FROM grouped_weather_data'
    result_df = pd.read_sql(query, conn)
    # Close the connection after use
    conn.close()
    return jsonify(result_df.to_dict(orient='records'))

# Endpoint to get location data
@api_routes.route('/weather_data_grouped', methods=['GET'])
def get_location_data():
    query = """
    SELECT * FROM (
        SELECT
            *,
            ROW_NUMBER() OVER(PARTITION BY nombre ORDER BY window_start DESC) as rn
        FROM grouped_weather_data
    ) t
    WHERE t.rn = 1
    """
    conn = create_connection_forest()
    result_df = pd.read_sql(query, conn)
    conn.close()
    return jsonify(result_df.to_dict(orient='records'))

# Endpoint para acceder a las especies de cada location
@api_routes.route('/mushroom-species', methods=['GET'])
def get_mushroom_species():
    location = request.args.get('location', '')  # Get the location parameter from the request
    conn = create_connection_forest()
    
    # Use parameterized query to filter by location
    query = 'SELECT * FROM mushroom_species_location WHERE location = ?'
    result_df = pd.read_sql(query, conn, params=(location,))
    
    conn.close()
    return jsonify(result_df.to_dict(orient='records'))



# Endpoint para registrar un nuevo usuario
@api_routes.route('/register', methods=['POST'])
def register_user():
    data = request.json  # Obtiene los datos del cuerpo de la solicitud
    username = data.get('username')
    password = data.get('password')
    
    # Crea una instancia de WeatherDatabase para interactuar con la base de datos
    # weather_db = WeatherDatabase()
    db_model = ForestModel(mysql_params)
    
    # Verifica si el nombre de usuario ya está en uso
    existing_user = db_model.get_user_by_username(username)
    if existing_user:
        return jsonify({'error': 'El nombre de usuario ya está en uso'}), 400
    
    # Inserta el nuevo usuario en la base de datos
    db_model.insert_user(username, password)
    
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

@api_routes.route('/login', methods=['POST'])
def login():
    # Obtener los datos del cuerpo de la solicitud
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Crea una instancia de WeatherDatabase para interactuar con la base de datos
    # weather_db = WeatherDatabase()
    db_model = ForestModel(mysql_params)

    # Buscar el usuario en la base de datos por su nombre de usuario
    usuario = db_model.get_user_pswd(username)
    print(usuario)
    if usuario:
        # Verificar la contraseña
        if usuario['password'] == password:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404
    

# Nuevo endpoint para obtener los primeros 10 registros de la tabla 'gis_forest'
'''@api_routes.route('/forest-data', methods=['GET'])
def get_forest_data():
    conn = create_connection_forest()  # Crear una nueva conexión SQLite para cada solicitud
    try:
        query = 'SELECT * FROM forest'  # Consulta para obtener los primeros 10 registros
        result_df = pd.read_sql(query, conn)
        return jsonify(result_df.to_dict(orient='records'))  # Devuelve los datos como JSON
    finally:
        conn.close()  # Cerrar la conexión después de usarla
        '''

@api_routes.route('/forest-data', methods=['GET'])
def get_forest_data():
    conn = create_connection_forest()
    try:
        query = 'SELECT * FROM forest'
        print("Executing query:", query)
        result_df = pd.read_sql(query, conn)
        print("Query executed successfully. Number of records fetched:", len(result_df))
        result_df = result_df.replace({np.nan: None})  # Replace NaN with None
        result_data = result_df.to_dict(orient='records')

        def is_valid_coordinate(coord):
            try:
                lng, lat = map(float, coord.split())
                return -180 <= lng <= 180 and -90 <= lat <= 90
            except:
                return False

        def replace_invalid_coordinates(coords):
            valid_coords = []
            last_valid_lat = None
            last_valid_lng = None

            for coord in coords:
                try:
                    lng, lat = map(float, coord.split())
                    if is_valid_coordinate(coord):
                        valid_coords.append(f"{lng} {lat}")
                        last_valid_lng, last_valid_lat = lng, lat
                    else:
                        raise ValueError("Invalid coordinate")
                except ValueError:
                    if last_valid_lng is not None and last_valid_lat is not None:
                        if np.isnan(lng) and not np.isnan(lat):
                            valid_coords.append(f"{last_valid_lng} {lat}")
                        elif not np.isnan(lng) and np.isnan(lat):
                            valid_coords.append(f"{lng} {last_valid_lat}")
                        elif np.isnan(lng) and np.isnan(lat):
                            valid_coords.append(f"{last_valid_lng} {last_valid_lat}")
                    else:
                        print("No valid previous coordinate to use as replacement")
                        return []  # Return an empty list if no valid coordinates

            return valid_coords

        for record in result_data:
            for key, value in record.items():
                if isinstance(value, bytes):
                    record[key] = value.decode('utf-8')
                elif key in ['altitude', 'centroide_lat', 'centroide_lng'] and value is not None:
                    record[key] = float(value)
                # Remove this block to avoid conversion
                # elif key == 'forest_id' and value is not None:
                #     record[key] = int(value)

            if 'polygon' in record and record['polygon']:
                coords = record['polygon'].replace("POLYGON ((", "").replace("))", "").split(", ")
                valid_coords = replace_invalid_coordinates(coords)
                if valid_coords:
                    record['polygon'] = f"POLYGON (({', '.join(valid_coords)}))"
                else:
                    record['polygon'] = None

        return jsonify(result_data)
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@api_routes.route('/weather-data-new', methods=['GET'])
def get_weather_data_new():
    # Create a new SQLite connection for each request
    conn = create_connection_forest()
    try:
        # Get the location_id parameter from the query string
        location_id = request.args.get('location_id', default=None, type=str)
        if not location_id:
            return jsonify({'error': 'location_id parameter is required'}), 400

        # Calculate the date 30 days ago from today
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Query to select data within the last 30 days for the specified location_id
        query = f'''
        SELECT * FROM weather 
        WHERE date >= "{thirty_days_ago}" 
        AND location_id = "{location_id}"
        '''
        
        result_df = pd.read_sql(query, conn)
        # Replace NaN with None for JSON serialization
        result_df = result_df.where(pd.notnull(result_df), None)
        return jsonify(result_df.to_dict(orient='records'))  # Return the data as JSON
    finally:
        conn.close()  # Close the connection after use

@api_routes.route('/mushroom-species-data', methods=['GET'])
def get_mushroom_species_data():
    conn = create_connection_forest()  # Crear una nueva conexión SQLite para cada solicitud
    try:
        query = 'SELECT * FROM mushroom_species'  # Consulta para obtener los primeros 10 registros
        result_df = pd.read_sql(query, conn)
        return jsonify(result_df.to_dict(orient='records'))  # Devuelve los datos como JSON
    finally:
        conn.close()  # Cerrar la conexión después de usarla


@api_routes.route('/mushroom-species-by-forest', methods=['GET'])
def get_mushroom_species_by_forest():
    tipo_bosque_id = request.args.get('tipo_bosque_id')
    if not tipo_bosque_id:
        return "Missing 'tipo_bosque_id' parameter", 400
    
    conn = create_connection_forest()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mushroom_species WHERE tipo_bosque_id = ?', (tipo_bosque_id,))
    rows = cursor.fetchall()

    # Retrieve column names
    columns = [column[0] for column in cursor.description]

    # Convert rows to a list of dictionaries
    mushrooms = [dict(zip(columns, row)) for row in rows]

    conn.close()
    return jsonify(mushrooms) if mushrooms else ("No mushrooms found for this forest type.", 404)

@api_routes.route('/mushroom-species-probabilities', methods=['GET'])
def get_mushroom_species_probabilities():
    tipo_bosque_id = request.args.get('tipo_bosque_id')
    if not tipo_bosque_id:
        return jsonify({'error': 'tipo_bosque_id is required'}), 400
    location_id = request.args.get('location_id')
    if not location_id:
        return jsonify({'error': 'location_id is required'}), 400

    conn = create_connection_forest()
    try:
        query = '''
        SELECT ms.specie_id, ms.specie_name, ms.temp_min, ms.temp_max, ms.prec_acc_min, ms.prec_acc_max, ms.altura_min, ms.altura_optima_min, ms.altura_optima_max, mp.probability
        FROM mushroom_species ms
        LEFT JOIN mushroom_probabilities mp ON ms.specie_id = mp.specie_id
        WHERE ms.tipo_bosque_id = %s
            AND mp.location_id = %s
        '''
        cursor = conn.cursor()
        cursor.execute(query, (tipo_bosque_id,location_id))
        rows = cursor.fetchall()
        # Retrieve column names
        columns = [column[0] for column in cursor.description]

        # Convert rows to a list of dictionaries
        mushrooms = [dict(zip(columns, row)) for row in rows]
        return jsonify(mushrooms)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        conn.close()

