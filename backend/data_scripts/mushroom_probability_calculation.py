#import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
import sqlalchemy
import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.db_config import mysql_params 

# Database path
#DB_PATH = 'forest_data.db'

def get_connection():
    return mysql.connector.connect(**mysql_params)

def get_sqlalchemy_engine():
    connection_string = f"mysql+mysqlconnector://{mysql_params['user']}:{mysql_params['password']}@{mysql_params['host']}:{mysql_params['port']}/{mysql_params['database']}"
    return sqlalchemy.create_engine(connection_string)

def fetch_recent_weather(location_id):
    engine = get_sqlalchemy_engine()
    today = datetime.today()
    fifteen_days_ago = today - timedelta(days=15)
    query = '''
        SELECT date, temp_min, temp_max, temp_avg, prec
        FROM weather
        WHERE location_id = %s AND date >= %s
        ORDER BY date DESC
    '''
    df = pd.read_sql(query, engine, params=(location_id, fifteen_days_ago.strftime('%Y-%m-%d')))
    return df

def fetch_mushroom_species(tipo_bosque_id):
    engine = get_sqlalchemy_engine()
    query = '''
        SELECT specie_id, specie_name, temp_min, temp_max, prec_acc_min, prec_acc_max, altura_min, altura_optima_min, altura_optima_max
        FROM mushroom_species
        WHERE tipo_bosque_id = %s
    '''
    df = pd.read_sql(query, engine, params=(tipo_bosque_id,))
    return df

def fetch_location_altitude(location_id):
    """Fetch the altitude for a given location_id from the database."""
    conn = get_connection()
    query = 'SELECT altitude, tipo_id FROM forest WHERE location_id = %s'
    cursor = conn.cursor()
    cursor.execute(query, (location_id,))
    results = cursor.fetchall()  # Consume todos los resultados
    cursor.close()
    conn.close()

    if not results:
        raise ValueError(f"No data found for location_id: {location_id}")

    if len(results[0]) != 2:
        raise ValueError(f"Unexpected number of columns returned for location_id {location_id}: {results[0]}")

    altitude, tipo_bosque_id = results[0]
    
    #if altitude is None:
    #    raise ValueError(f"Altitude is None for location_id: {location_id}")
    
    return float(altitude), tipo_bosque_id

def calculate_probabilities(location_id):
    try:
        location_altitude, tipo_bosque_id = fetch_location_altitude(location_id)
    except ValueError as e:
        print(e)
        return []  # Devuelve un iterable vacío en caso de error

    weather_data = fetch_recent_weather(location_id)
    mushroom_species = fetch_mushroom_species(tipo_bosque_id)

    results = []
    seven_days_ago = datetime.today() - timedelta(days=7)

    # Convert 'date' column to datetime
    weather_data['date'] = pd.to_datetime(weather_data['date'])

    weather_data['period'] = weather_data['date'].apply(lambda x: 'recent' if x >= seven_days_ago else 'previous')

    for _, specie in mushroom_species.iterrows():
        # Altitude check
        if not (specie['altura_min'] <= location_altitude <= specie['altura_optima_max']):
            probability = "0 probabilities"
            results.append({"specie_name": specie['specie_name'], "probability": probability})
            continue
        
        counts = {
            'recent_temp': 0,
            'previous_temp': 0,
            'recent_prec': 0,
            'previous_prec': 0,
            'total_prec': 0
        }
        
        weather_data['temp_avg'] = pd.to_numeric(weather_data['temp_avg'], errors='coerce')
        weather_data['prec'] = pd.to_numeric(weather_data['prec'], errors='coerce')

        for _, weather in weather_data.iterrows():
            if specie['temp_min'] <= weather['temp_avg'] <= specie['temp_max']:
                if weather['period'] == 'recent':
                    counts['recent_temp'] += 1
                else:
                    counts['previous_temp'] += 1

            if specie['prec_acc_min'] <= weather['prec'] <= specie['prec_acc_max']:
                if weather['period'] == 'recent':
                    counts['recent_prec'] += 1
                else:
                    counts['previous_prec'] += 1
        
        # Classify probability based on counts
        criteria_met = sum(1 for key, count in counts.items() if count > 0)
        if criteria_met == 5:
            probability = "High"
        elif criteria_met >= 3:
            probability = "Medium"
        elif criteria_met >= 1:
            probability = "Low"
        else:
            probability = "0 probabilities"

        results.append({"specie_name": specie['specie_name'], "probability": probability})

    return results


if __name__ == '__main__':
    location_id = "40.62456834443036_-4.160302287811402"  # Example ID
    probabilities = calculate_probabilities(location_id)
    print(probabilities)
