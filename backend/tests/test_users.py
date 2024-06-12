import sqlite3
import pandas as pd
import sys
import os 

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.models import WeatherDatabase

weather_db = WeatherDatabase()
#weather_db.insert_user('ejemplo_usuario', 'contraseña_secreta')

user = weather_db.get_user_by_username('irenemart')
print(user)  # Esto imprimirá la información del usuario si se encuentra, o None si no se encuentra
