import requests

# Make a GET request to the Flask API
api_url = 'http://127.0.0.1:5000/weather-data_grouped'  # Assuming Flask app is running locally on the default port
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the JSON response
    data = response.json()
    for record in data:
        print(record)
else:
    print(f"Error: Unable to fetch weather data. Status code: {response.status_code}")
