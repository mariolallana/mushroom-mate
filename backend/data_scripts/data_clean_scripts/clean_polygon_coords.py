import pandas as pd
from shapely.geometry import Polygon, Point
from shapely import wkt
import mysql.connector
from sqlalchemy import create_engine
import sys
import os

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

from api.controllers.db_config import mysql_params

# Conexión a la base de datos usando SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{mysql_params["user"]}:{mysql_params["password"]}@{mysql_params["host"]}/{mysql_params["database"]}')

#4949647.433125817_-451227.2051497749
#4955087.830086993_-425958.6985954832

def fetch_forest_data():
    query = '''
        SELECT 
            location_id, 
            polygon 
        FROM forest
        WHERE location_id = "4949647.433125817_-451227.2051497749"
    '''
    df = pd.read_sql(query, engine)
    return df

# Leer los datos de la tabla 'forest'
df = fetch_forest_data()

# Inspeccionar los datos para entender el formato
print("Datos de polygon:")
print(df['polygon'].head())

# Función para verificar y limpiar los datos
def check_and_clean_data(wkt_str):
    try:
        if not wkt_str.startswith("POLYGON"):
            return None
        coordinates = wkt_str.lstrip("POLYGON ((").rstrip("))").split(", ")
        cleaned_coordinates = []
        for pair in coordinates:
            try:
                if len(pair.split(" ")) != 2:
                    continue
                lng, lat = pair.split(" ")
                lng = float(lng)
                lat = float(lat)
                if -180 <= lng <= 180 and -90 <= lat <= 90:
                    cleaned_coordinates.append(f"{lng} {lat}")
            except ValueError:
                continue
        
        # Asegurarnos de que el polígono esté cerrado
        if cleaned_coordinates[0] != cleaned_coordinates[-1]:
            cleaned_coordinates.append(cleaned_coordinates[0])
        
        if len(cleaned_coordinates) >= 4:  # Un polígono necesita al menos 4 puntos válidos (3 puntos más el punto de cierre)
            cleaned_wkt_str = f"POLYGON (({', '.join(cleaned_coordinates)}))"
            return cleaned_wkt_str
        else:
            return None
    except Exception as e:
        print(f"Error checking data validity: {e}")
        return None

# Convertir datos de bytes a string y luego a WKT usando shapely
def convert_bytes_to_wkt(bytes_data):
    try:
        # Decodificar bytes a string
        wkt_str = bytes_data.decode('utf-8')
        # Imprimir para inspección
        #print(f"Decoded WKT string: {wkt_str}")
        # Verificar y limpiar los datos
        cleaned_wkt_str = check_and_clean_data(wkt_str)
        if not cleaned_wkt_str:
            print("Datos de coordenadas no válidos o incompletos.")
            return None
        # Convertir string a objeto geométrico WKT
        geom = wkt.loads(cleaned_wkt_str)
        return geom.wkt
    except Exception as e:
        print(f"Error converting bytes to WKT: {e}")
        return None

# Aplicar la conversión
df['polygon_wkt'] = df['polygon'].apply(convert_bytes_to_wkt)

# Imprimir para verificación
print(df[['location_id', 'polygon_wkt']].head())

# Función para limpiar coordenadas erróneas
def clean_polygon(wkt_str):
    try:
        polygon = wkt.loads(wkt_str)
        cleaned_points = []
        for lng, lat in polygon.exterior.coords:
            if -180 <= lng <= 180 and -90 <= lat <= 90:
                cleaned_points.append((lng, lat))
        if len(cleaned_points) >= 4:  # Un polígono necesita al menos 4 puntos válidos (3 puntos más el punto de cierre)
            return Polygon(cleaned_points)
        else:
            return None
    except Exception as e:
        print(f"Error cleaning polygon: {e}")
        return None

# Aplicar la limpieza a cada polígono
df['cleaned_polygon'] = df['polygon_wkt'].apply(clean_polygon)

# Filtrar los registros con polígonos válidos
df_valid = df[df['cleaned_polygon'].notnull()]

# Conexión a la base de datos usando SQLAlchemy para actualizar registros
for _, row in df_valid.iterrows():
    cleaned_wkt = row['cleaned_polygon'].wkt
    update_query = f"""
    UPDATE forest
    SET polygon = ST_GeomFromText('{cleaned_wkt}', 4326)
    WHERE location_id = '{row['location_id']}'
    """
    with engine.connect() as conn:
        conn.execute(update_query)
