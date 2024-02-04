import requests
import pandas as pd

####################################################
## 1 ## Parte de consulta de datos de API y limpieza
####################################################

# URL de la primera solicitud
url_inicial = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fecha" \
              "ini/2024-01-06T00%3A00%3A00UTC/fechafin/2024-01-16T23%3A59%3A00UTC/estacion/2462%2C3111D%2C3266A%2C3110C" \
              "/?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYXJpb2xhbGxhbmExMkBnbWFpbC5jb20iLCJqdGkiOiIyMDViNzYyNS00NGU5LTRhYTUtYWMwMi04NGE5YmRlMzhmNjIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcwNTUyODUwNSwidXNlcklkIjoiMjA1Yjc2MjUtNDRlOS00YWE1LWFjMDItODRhOWJkZTM4ZjYyIiwicm9sZSI6IiJ9.m5VUOP_qqVXBEiM5Iex2EoLYGUeaf0qfmey2EC62GeI"

# Hacer la primera solicitud
response = requests.get(url_inicial)

# Obtener el enlace del siguiente URL desde el resultado de la primera solicitud
next_url = response.json()["datos"]

# Hacer la segunda solicitud
response = requests.get(next_url)

# Convertir el contenido JSON en un DataFrame de pandas
df = pd.DataFrame(response.json())

# Imprimir el DataFrame
#print(df)

# Me quedo con las columnas que nedecesito
df = df[['fecha','indicativo','nombre','provincia','tmed','prec']]

# Convertir las columnas 'prec' y 'tmed' a tipo float
df['prec'] = df['prec'].str.replace(',', '.').astype(float)
df['tmed'] = df['tmed'].str.replace(',', '.').astype(float)

# Convertir la columna de fechas a tipo datetime si aún no está en ese formato
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')


####################################################
## 2 ## Parte de setup de back end DB
####################################################

import sqlite3

# Create a SQLite database connection
conn = sqlite3.connect('weather_data.db')

# Define the table schema
create_table_query = '''
CREATE TABLE IF NOT EXISTS weather_data (
    fecha TIMESTAMP,
    indicativo TEXT,
    nombre TEXT,
    provincia TEXT,
    tmed REAL,
    prec REAL
);
'''

# Execute the query to create the table
conn.execute(create_table_query)

# Insert the DataFrame into the SQLite table
df.to_sql('weather_data', conn, if_exists='replace', index=False)

# Example: Query all data from the table
query = 'SELECT * FROM weather_data WHERE tmed > 0'
result_df = pd.read_sql(query, conn)
##print(result_df)

