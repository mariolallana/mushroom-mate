#import sqlite3
import requests
from opencage.geocoder import OpenCageGeocode

# Connect to the SQLite database
#conn = sqlite3.connect('weather_data.db')
#cursor = conn.cursor()

# Replace 'YOUR_OPENCAGE_API_KEY' with your actual OpenCage API key
opencage_api_key = '579ed71853024fa7ba52ca7e51346894'
geocoder = OpenCageGeocode(opencage_api_key)

# Function to get coordinates and altitude
def get_coordinates_and_altitude(locations_df):
    results = []
    for index, row in locations_df.iterrows():
        location_name = str(row['location_name'])
        result = geocoder.geocode(location_name)
        if result and len(result):
            location = result[0]['geometry']
            lat, lng = location['lat'], location['lng']

            # Get altitude using Open-Elevation API
            elevation_api_url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lng}"
            elevation_data = requests.get(elevation_api_url).json()
            altitude = elevation_data['results'][0]['elevation'] if elevation_data and 'results' in elevation_data else None

            results.append((lat, lng, altitude, row['location_id']))
        else:
            results.append((None, None, None, row['location_id']))
    
    return results

'''
# Update existing table with latitude, longitude, and altitude data
cursor.execute('SELECT indicativo as location_id, nombre as location_name FROM weather_data_grouped')
rows = cursor.fetchall()

for row in rows:
    location_id, location_name = row
    coordinates_and_altitude = get_coordinates_and_altitude(location_name)

    if coordinates_and_altitude:
        lat, lng, altitude = coordinates_and_altitude
        cursor.execute('UPDATE weather_data_grouped SET latitude=?, longitude=?, altitude=? WHERE indicativo=?',
                       (lat, lng, altitude, location_id))

# Commit the changes and close the connection
conn.commit()
conn.close()
'''