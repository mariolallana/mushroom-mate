# backend/src/data_scripts/populate_mushroom_species.py

import sys
import os
import pandas as pd
from tabulate import tabulate

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

# Now 'backend' directory should be in sys.path
#print(sys.path)

from data_scripts.fetch_data import fetch_data
from api.controllers.models import WeatherDatabase 

# def print_mushroom_species_table():
#     query = 'SELECT * FROM mushroom_species_location'
#     df_mushroom = pd.read_sql_query(query, weather_db.conn)
#     print(tabulate(df_mushroom, headers='keys', tablefmt='psql'))

def populate_species_table():
    mushroom_species = [
        ("Boletus edulis", "/path/to/photo1.jpg", "Alta", "Excelente", "PUERTO DE NAVACERRADA"),
        ("Amanita muscaria", "/path/to/photo2.jpg", "Media", "Tóxica", "PUERTO DE NAVACERRADA"),
        ("Cantharellus cibarius", "/path/to/photo3.jpg", "Baja", "Bueno", "PUERTO DE NAVACERRADA"),
        ("Russula cyanoxantha", "/path/to/photo4.jpg", "Media", "Excelente", "PUERTO DE NAVACERRADA"),
        ("Lactarius deliciosus", "/path/to/photo5.jpg", "Alta", "Bueno", "PUERTO DE NAVACERRADA"),
        ("Tricholoma terreum", "/path/to/photo6.jpg", "Media", "Mediocre", "BUITRAGO DEL LOZOYA"),
        ("Hydnum repandum", "/path/to/photo7.jpg", "Baja", "Bueno", "BUITRAGO DEL LOZOYA"),
        ("Agaricus campestris", "/path/to/photo8.jpg", "Alta", "Excelente", "BUITRAGO DEL LOZOYA"),
        ("Morchella esculenta", "/path/to/photo9.jpg", "Baja", "Excelente", "BUITRAGO DEL LOZOYA"),
        ("Clitocybe nuda", "/path/to/photo10.jpg", "Media", "Bueno", "BUITRAGO DEL LOZOYA"),
        ("Pleurotus ostreatus", "/path/to/photo11.jpg", "Alta", "Excelente", "SOMOSIERRA"),
        ("Calocybe gambosa", "/path/to/photo12.jpg", "Baja", "Mediocre", "SOMOSIERRA"),
        ("Boletus aereus", "/path/to/photo13.jpg", "Media", "Excelente", "SOMOSIERRA"),
        ("Amanita caesarea", "/path/to/photo14.jpg", "Baja", "Excelente", "SOMOSIERRA"),
        ("Macrolepiota procera", "/path/to/photo15.jpg", "Alta", "Bueno", "SOMOSIERRA"),
        ("Suillus luteus", "/path/to/photo16.jpg", "Media", "Mediocre", "PUERTO ALTO DEL LEÓN"),
        ("Coprinus comatus", "/path/to/photo17.jpg", "Alta", "Bueno", "PUERTO ALTO DEL LEÓN"),
        ("Boletus pinophilus", "/path/to/photo18.jpg", "Baja", "Excelente", "PUERTO ALTO DEL LEÓN"),
        ("Craterellus cornucopioides", "/path/to/photo19.jpg", "Media", "Sin interés", "PUERTO ALTO DEL LEÓN"),
        ("Agaricus arvensis", "/path/to/photo20.jpg", "Alta", "Bueno", "PUERTO ALTO DEL LEÓN"),
    ]


    # Create an instance of WeatherDatabase
    weather_db = WeatherDatabase()

    # Primero, asegúrate de que la tabla existe
    weather_db.create_mushroom_species_table()

    # Ejemplo para insertar datos dummy
    for species in mushroom_species:
        weather_db.insert_mushroom_species(species)

    #print_mushroom_species_table()