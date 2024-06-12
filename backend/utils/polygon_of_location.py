import numpy as np
import pandas as pd
import requests
from scipy.spatial import ConvexHull
from concurrent.futures import ThreadPoolExecutor

def get_altitude(lat, lng):
    response = requests.get(f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lng}")
    if response.status_code == 200:
        elevation_data = response.json()
        return elevation_data['results'][0]['elevation']
    else:
        return None

def fetch_altitudes(df):
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(get_altitude, row['Latitude'], row['Longitude']) for index, row in df.iterrows()]
        for future, row in zip(futures, df.iterrows()):
            df.at[row[0], 'Altitude'] = future.result()
    return df

def get_polygon_points(start_point):
    step_size = 300
    area_size = 3000

    METERS_PER_DEGREE_LAT = 111320
    METERS_PER_DEGREE_LNG = 111320 * np.cos(np.radians(start_point['lat']))

    steps = int(area_size / step_size)

    latitudes = np.linspace(start_point['lat'] - steps * (step_size / METERS_PER_DEGREE_LAT),
                            start_point['lat'] + steps * (step_size / METERS_PER_DEGREE_LAT),
                            2 * steps + 1)
    longitudes = np.linspace(start_point['lng'] - steps * (step_size / METERS_PER_DEGREE_LNG),
                             start_point['lng'] + steps * (step_size / METERS_PER_DEGREE_LNG),
                             2 * steps + 1)

    points = np.array(np.meshgrid(latitudes, longitudes)).T.reshape(-1, 2)

    df = pd.DataFrame(points, columns=['Latitude', 'Longitude'])

    # Fetch altitudes in parallel
    df = fetch_altitudes(df)

    df_cleaned = df.dropna()

    df_cleaned['AltitudeDiff'] = df_cleaned['Altitude'] - start_point['alt']
    filtered_points = df_cleaned[(df_cleaned['AltitudeDiff'] >= -100) & (df_cleaned['AltitudeDiff'] <= 100)]

    points = np.array(filtered_points[['Latitude', 'Longitude']])
    hull = ConvexHull(points)

    polygon_lat = points[hull.vertices, 0].tolist() + [points[hull.vertices[0], 0]]
    polygon_lng = points[hull.vertices, 1].tolist() + [points[hull.vertices[0], 1]]

    return polygon_lat, polygon_lng

# Example usage
start_point = {'lat': 40.78887, 'lng': -4.00373, 'alt': 1863}
polygon_lat, polygon_lng = get_polygon_points(start_point)

polygon_lat, polygon_lng