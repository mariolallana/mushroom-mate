from flask import Blueprint, jsonify, request
import sqlite3
import pandas as pd
import os
import sys

api_routes = Blueprint('api_routes', __name__)

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import WeatherDatabase

# Function to create and return a SQLite connection
def create_connection():
    return sqlite3.connect('weather_data.db')

# Endpoint to get weather data
@api_routes.route('/weather-data', methods=['GET'])
def get_weather_data():
    # Create a new SQLite connection for each request
    conn = create_connection()
    query = 'SELECT * FROM weather_data'
    result_df = pd.read_sql(query, conn)
    # Close the connection after use
    conn.close()
    return jsonify(result_df.to_dict(orient='records'))
    
# Endpoint to get location data
@api_routes.route('/weather_data_grouped', methods=['GET'])
def get_location_data():
    query = 'SELECT * FROM grouped_weather_data '
    conn = create_connection()
    result_df = pd.read_sql(query, conn)
    conn.close()
    return jsonify(result_df.to_dict(orient='records'))

# Endpoint para registrar un nuevo usuario
@api_routes.route('/register', methods=['POST'])
def register_user():
    data = request.json  # Obtiene los datos del cuerpo de la solicitud
    username = data.get('username')
    password = data.get('password')
    
    # Crea una instancia de WeatherDatabase para interactuar con la base de datos
    weather_db = WeatherDatabase()
    
    # Verifica si el nombre de usuario ya está en uso
    existing_user = weather_db.get_user_by_username(username)
    if existing_user:
        return jsonify({'error': 'El nombre de usuario ya está en uso'}), 400
    
    # Inserta el nuevo usuario en la base de datos
    weather_db.insert_user(username, password)
    
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

@api_routes.route('/login', methods=['POST'])
def login():
    # Obtener los datos del cuerpo de la solicitud
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Crea una instancia de WeatherDatabase para interactuar con la base de datos
    weather_db = WeatherDatabase()

    # Buscar el usuario en la base de datos por su nombre de usuario
    usuario = weather_db.get_user_pswd(username)
    print(usuario)
    if usuario:
        # Verificar la contraseña
        if usuario['password'] == password:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404

