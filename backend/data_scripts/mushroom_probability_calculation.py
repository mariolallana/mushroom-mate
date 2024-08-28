#import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
import sqlalchemy
import sys
import os
from typing import List, Dict, Any

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.db_config import connection_pool
from data_scripts.database_utils import get_connection, get_sqlalchemy_engine, close_connection

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        SELECT specie_id, specie_name, temp_min, temp_max, prec_acc_min, prec_acc_max, altura_optima_min, altura_optima_max, altura_max
        FROM mushroom_species
        WHERE tipo_bosque_id = %s
    '''
    #logger.info(f"Executing query: {query} with tipo_bosque_id: {tipo_bosque_id}")
    df = pd.read_sql(query, engine, params=(tipo_bosque_id,))
    #logger.info(f"Query result: {df}")
    return df

def fetch_location_altitude(location_id):
    """Fetch the altitude for a given location_id from the database."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        query = 'SELECT altitude, tipo_id FROM forest WHERE location_id = %s'
        cursor.execute(query, (location_id,))
        results = cursor.fetchall()

        if not results:
            raise ValueError(f"No data found for location_id: {location_id}")

        if len(results[0]) != 2:
            raise ValueError(f"Unexpected number of columns returned for location_id {location_id}: {results[0]}")

        altitude, tipo_bosque_id = results[0]
        return float(altitude), tipo_bosque_id
    finally:
        cursor.close()
        close_connection(conn)

def calculate_probabilities(location_id: str) -> List[Dict[str, Any]]:
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
        if not (specie['altura_optima_min'] <= location_altitude <= specie['altura_optima_max']):
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
    location_id = "4991328.055944796_-415861.93555245845"  # Example ID
    probabilities = calculate_probabilities(location_id)
    print(probabilities)
