# backend/src/data_scripts/fetch_data.py
import requests
import pandas as pd

def fetch_data(api_key, start_date, end_date, station_ids):
    # Convert station IDs to a comma-separated string
    array_idemas = "%2C".join(station_ids)

    # Construct the URL
    url_inicial = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{start_date}/fechafin/{end_date}/estacion/{array_idemas}/?api_key={api_key}"

    response = requests.get(url_inicial)
    response_json = response.json()

    # Check if 'datos' key is present
    if 'datos' in response_json:
        next_url = response_json["datos"]
        response = requests.get(next_url)
        df = pd.DataFrame(response.json())
        df = df[['fecha', 'indicativo', 'nombre', 'provincia', 'tmed', 'prec']]
        df['prec'] = df['prec'].str.replace(',', '.')
        df['prec'] = pd.to_numeric(df['prec'], errors='coerce')
        df['tmed'] = df['tmed'].str.replace(',', '.').astype(float)
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

        return df
    else:
        print("Error: 'datos' key not found in the response.")
        return None
