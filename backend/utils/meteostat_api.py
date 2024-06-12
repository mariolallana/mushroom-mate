from meteostat import Point, Daily
from datetime import datetime
import pandas as pd



# Find the closest station to Barcelona, Spain
location = Point(40.7889324, -4.0035946)  # Latitude & Longitude of Barcelona

# Set time period
start = datetime(2024, 3, 1)
end = datetime(2024, 3, 31)

# Get daily data
data = Daily(location, start, end)
data = data.fetch()

print(data)
