# backend/src/api/controllers/models.py
import sqlite3
import datetime
import pandas as pd
from tabulate import tabulate


class WeatherDatabase:
    def __init__(self, db_path='weather_data.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_weather_data_table()
        self.create_grouped_weather_data_table()
        self.create_users_table() 

    def create_weather_data_table(self):
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
        self.conn.execute(create_table_query)
    
    def drop_weather_table(self):
        drop_table_query = '''
        DROP TABLE IF EXISTS weather_data;
        '''
        self.conn.execute(drop_table_query)

    def drop_grouped_weather_table(self):
        drop_table_query = '''
        DROP TABLE IF EXISTS grouped_weather_data;
        '''
        self.conn.execute(drop_table_query)

    def create_grouped_weather_data_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS grouped_weather_data (
           indicativo TEXT, 
           nombre TEXT, 
           provincia TEXT,
           window_start TIMESTAMP,
           total_prec REAL,
           media_diaria_prec REAL,
           min_tmed REAL,
           max_tmed REAL,
           media_tmed REAL,
           latitude REAL,
           longitude REAL,
           altitude REAL
        );
        '''
        self.conn.execute(create_table_query)

    def insert_weather_data(self, data):
        # Assuming data is a dictionary with keys corresponding to table columns
        # Adjust this according to the actual structure of your data
        insert_query = '''
        INSERT INTO weather_data (fecha, indicativo, nombre, provincia, tmed, prec)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        # Convertir el objeto Timestamp a un formato de fecha y hora compatible con SQLite
        fecha_str = data['fecha'].strftime('%Y-%m-%d %H:%M:%S')

        self.conn.execute(insert_query, (fecha_str, data['indicativo'], data['nombre'],
                                         data['provincia'], data['tmed'], data['prec']))
        self.conn.commit()

    def query_grouped_data(self):
        grouped_query = '''
        SELECT 
            indicativo, 
            nombre, 
            provincia,
            strftime('%Y-%m-%d', fecha, 'start of day', '-1 day', 'weekday 1', '+14 days') as window_start,
            SUM(prec) as total_prec,
            AVG(prec) as media_diaria_prec,
            MIN(tmed) as min_tmed,
            MAX(tmed) as max_tmed,
            AVG(tmed) as media_tmed,
            0.0 as latitude,
            0.0 as longitude,
            0.0 as altitude
        FROM 
            weather_data
        GROUP BY 
            indicativo, 
            nombre, 
            provincia,
            window_start
        '''
        df_grouped = pd.read_sql_query(grouped_query, self.conn)
        return df_grouped

    def insert_grouped_weather_data(self,data):
        # Define the insert query
        insert_query = """
        INSERT INTO grouped_weather_data (indicativo, nombre, provincia, window_start, 
                                        total_prec, media_diaria_prec, min_tmed, 
                                        max_tmed, media_tmed, latitude, longitude, altitude) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        # Execute the query with data as parameters
        self.conn.execute(insert_query, (data['indicativo'], data['nombre'], data['provincia'],
                                    data['window_start'], data['total_prec'], 
                                    data['media_diaria_prec'], data['min_tmed'], 
                                    data['max_tmed'], data['media_tmed'], 
                                    data['latitude'], data['longitude'], 
                                    data['altitude']))
        self.conn.commit()

    def query_all_locations_gw_data(self):
        query = 'SELECT indicativo as location_id, nombre as location_name FROM grouped_weather_data'
        df_query = pd.read_sql_query(query, self.conn)
        return df_query

    def update_grouped_weather_data_geo(self, locations_data):
        for location_data in locations_data:
            lat, lng, altitude, location_id = location_data
            self.conn.execute('UPDATE grouped_weather_data SET latitude=?, longitude=?, altitude=? WHERE indicativo=?',
                            (lat, lng, altitude, location_id))
        # Commit the changes and close the connection
        self.conn.commit()

    def create_users_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        );
        '''
        self.conn.execute(create_table_query)

    def insert_user(self, username, password):
        insert_query = '''
        INSERT INTO users (username, password)
        VALUES (?, ?)
        '''
        self.conn.execute(insert_query, (username, password))
        self.conn.commit()

    def get_user_by_username(self, username):
        query = 'SELECT * FROM users WHERE username = ?'
        result = self.conn.execute(query, (username,))
        user = result.fetchone()
        return user

    def get_user_pswd(self, username):
        cursor = self.conn.cursor()
        query = 'SELECT username, password FROM users WHERE username = ?'
        cursor.execute(query, (username,))
        usuario = cursor.fetchone()
        cursor.close()
        if usuario:
            return {'username': usuario[0], 'password': usuario[1]}
        else:
            return None

    def close_connection(self):
        self.conn.close()

# Example usage:
'''
if __name__ == "__main__":
    # Create an instance of WeatherDatabase
    weather_db = WeatherDatabase()

    # Example data to insert
    sample_data = {
        'fecha': '2024-02-04',
        'indicativo': '12345',
        'nombre': 'City1',
        'provincia': 'Province1',
        'tmed': 20.5,
        'prec': 5.0
    }

    # Insert sample data
    weather_db.insert_weather_data(sample_data)

    # Query grouped data
    grouped_data = weather_db.query_grouped_data()

    # Print the result
    print(tabulate(grouped_data, headers='keys', tablefmt='psql'))

    # Close the connection
    weather_db.close_connection()
'''