import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch_elevation(lat, lng, retries=3):
    elevation_api_url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lng}"
    for attempt in range(retries):
        try:
            response = requests.get(elevation_api_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            elevation_data = response.json()
            if 'results' in elevation_data and len(elevation_data['results']) > 0:
                return elevation_data['results'][0]['elevation']
            else:
                print(f"No results found in API response for {lat}, {lng}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}, attempt {attempt + 1}")
        except ValueError as e:
            print(f"Value error: {e}, attempt {attempt + 1}")
        time.sleep(2 ** attempt)  # Exponential backoff
    return None

def get_elevation_bulk(locations, elevation_cache):
    uncached_locations = [loc for loc in locations if loc not in elevation_cache]
    
    if not uncached_locations:
        return [elevation_cache[loc] for loc in locations]
    
    for lat, lng in uncached_locations:
        elevation = fetch_elevation(lat, lng)
        elevation_cache[(lat, lng)] = elevation
    
    return [elevation_cache.get(loc) for loc in locations]

def test_get_elevation_bulk():
    # Define a larger set of test locations
    test_locations = [
        (39.90578228589032, -3.812278143098061),
        (40.62456834443036, -4.160302287811402),
        (40.616118783550725, -4.158308892897453),
        (40.59413627264435, -4.16619059552512),
        (40.621420633168256, -4.149831287438076),
        (39.856648, -4.022458),
        (40.396764, -3.702056),
        (40.416775, -3.703790),
        (39.469907, -0.376288),
        (41.385064, 2.173404),
        (37.774929, -122.419418),
        (34.052235, -118.243683),
        (51.507351, -0.127758),
        (48.856613, 2.352222),
        (35.689487, 139.691711),
        (55.755825, 37.617298),
        (52.520008, 13.404954),
        (40.712776, -74.005974),
        (34.052235, -118.243683),
        (19.432608, -99.133209),
        (45.421532, -75.697189),
        (39.904202, 116.407394),
        (28.613939, 77.209023),
        (35.689487, 139.691711),
        (55.755825, 37.617298),
        (52.520008, 13.404954),
        (40.712776, -74.005974),
        (34.052235, -118.243683),
        (19.432608, -99.133209),
        (45.421532, -75.697189),
        (39.904202, 116.407394),
        (28.613939, 77.209023),
        (35.689487, 139.691711),
        (55.755825, 37.617298),
        (52.520008, 13.404954),
        (40.712776, -74.005974),
        (34.052235, -118.243683),
        (19.432608, -99.133209),
        (45.421532, -75.697189),
        (39.904202, 116.407394),
        (28.613939, 77.209023),
        (35.689487, 139.691711),
        (55.755825, 37.617298),
        (52.520008, 13.404954),
        (40.712776, -74.005974),
        (34.052235, -118.243683),
        (19.432608, -99.133209),
        (45.421532, -75.697189),
        (39.904202, 116.407394),
        (28.613939, 77.209023)
    ]
    
    # Create an empty elevation cache
    elevation_cache = {}
    
    # Fetch elevations in bulk
    start_time = time.time()
    elevations = get_elevation_bulk(test_locations, elevation_cache)
    end_time = time.time()
    
    # Print the results
    for loc, elev in zip(test_locations, elevations):
        print(f"Location: {loc}, Elevation: {elev}")
    
    print(f"Time taken for fetching elevations: {end_time - start_time} seconds")

if __name__ == '__main__':
    test_get_elevation_bulk()
