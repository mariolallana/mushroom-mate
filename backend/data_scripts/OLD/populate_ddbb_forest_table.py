import os
import sys
import sqlite3
import geopandas as gpd
import pandas as pd

# Get the absolute path of the 'backend' directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

# Importar desde el backend
from data_scripts.fetch_data import fetch_data
from api.controllers.models import GISForestModel 

def prepare_data(file_path):
    try:
        datos_gis = gpd.read_file(file_path)
        print("Datos cargados correctamente.")
        print(f"Primeras geometrías: {datos_gis.geometry.head()}")

        if datos_gis.crs != 'epsg:4326':
            datos_gis = datos_gis.to_crs('epsg:4326')
        print("Conversión de CRS realizada.")

        datos_gis_bosques = datos_gis.loc[datos_gis['FormArbol'].str.contains("Pinar", na=False) &
                                          (datos_gis['DesTipEstr'].isin(["Bosque"]))]

        print(f"Filtrado realizado, número de registros: {len(datos_gis_bosques)}")

        if not datos_gis_bosques.empty:
            # Utilizar 'apply' directamente dentro de una nueva asignación para evitar problemas
            geometries_wkt = datos_gis_bosques['geometry'].apply(lambda geom: geom.wkt)
            datos_gis_bosques = pd.DataFrame({
                'FormArbol': datos_gis_bosques['FormArbol'],
                'geometry': geometries_wkt
            })
            print("Conversión a WKT realizada.")
        else:
            print("No hay geometrías para convertir.")

        return datos_gis_bosques
    except Exception as e:
        print(f"Error al preparar los datos: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

def populate_forest_table():
    # Path to the GIS file
    file_path = r'C:\Users\mario\Downloads\mfe_madrid\MFE_30.shp'
    
    # Preparar los datos
    prepared_data = prepare_data(file_path)
    
    if not prepared_data.empty:
        try:
            # Conectar a la base de datos SQLite
            conn = sqlite3.connect('forest_data.db')
            db_model = GISForestModel(conn)
            
            # Insertar datos en la base de datos
            for row in prepared_data.itertuples(index=False, name=None):
                db_model.insert_gis_forest_data(row)

        except sqlite3.Error as e:
            print(f"Error al conectar o manipular la base de datos: {e}")
        finally:
            # Cerrar la conexión a la base de datos
            conn.close()
    else:
        print("No hay datos para insertar.")

