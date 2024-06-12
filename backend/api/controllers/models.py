# backend/src/api/controllers/models.py
#import sqlite3
import mysql.connector
from datetime import datetime
import pandas as pd
from tabulate import tabulate
#from api.controllers.db_config import mysql_params 

MAX_POLYGON_LENGTH = 65535  # Tamaño máximo para un campo TEXT

class ForestModel:
    def __init__(self, mysql_params, connection=None):
        if connection:
            self.conn = connection
        else:
            self.conn = mysql.connector.connect(**mysql_params)

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
                       
    def create_tables(self):
        cursor = self.conn.cursor()
        # Create forest table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS forest (
            forest_id VARCHAR(255) PRIMARY KEY,
            tipo_id INTEGER,
            tipo_desc TEXT,
            centroide_lat FLOAT,
            centroide_lng FLOAT,
            polygon LONGBLOB,
            altitude FLOAT,
            location_id VARCHAR(255),
            INDEX(location_id)  -- Agrega un índice en location_id
        );
        ''')

        # Create weather table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            weather_id VARCHAR(255) PRIMARY KEY,
            location_id VARCHAR(255);
            date DATE,
            temp_min FLOAT,
            temp_max FLOAT,
            temp_avg FLOAT,
            prec FLOAT,
            prec_acc_3_days FLOAT,
            prec_acc_7_days FLOAT,
            prec_acc_15_days FLOAT,
            FOREIGN KEY(location_id) REFERENCES forest(location_id)
        );
        ''')

        # Create mushroom_species table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mushroom_species (
            specie_id INTEGER PRIMARY KEY,
            specie_name TEXT,
            specie_desc TEXT,
            tipo_bosque_id INTEGER,
            temp_max FLOAT,
            temp_min FLOAT,
            prec_acc_min INTEGER,
            prec_acc_max INTEGER,
            altura_optima_max FLOAT,
            altura_optima_min FLOAT,
            altura_min FLOAT,
        );
        ''')

        self.conn.commit()

    def drop_all_tables(self):
        # List all tables related to the forest data to be dropped
        tables = ['forest']  # Add more table names as needed
        for table in tables:
            self.conn.execute(f'DROP TABLE IF EXISTS {table};')
        self.conn.commit()

    def create_mushroom_species_table(self):
        # Create mushroom_species table
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mushroom_species (
            specie_id INTEGER PRIMARY KEY,
            specie_name TEXT,
            specie_desc TEXT,
            tipo_bosque_id INTEGER,
            temp_max FLOAT,
            temp_min FLOAT,
            prec_acc_min INTEGER,
            prec_acc_max INTEGER,
            altura_optima_max FLOAT,
            altura_optima_min FLOAT,
            altura_min FLOAT
        );
        ''')
        self.conn.commit()  # Commit changes
    
    def create_mushroom_probability(self):
        # Create mushroom_probabilities table
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS mushroom_probabilities (
                location_id VARCHAR(255),
                specie_id INTEGER,
                probability TEXT,
                last_updated TIMESTAMP
            );
            ''')
            self.conn.commit()  # Commit changes
            print("Table created or already exists.")
        except mysql.connector.Error as err:
            print("Error creating table:", err)
            self.conn.rollback()
        finally:
            cursor.close()


    def update_probability_record(self, location_id, specie_id, probability):
        current_time = datetime.now()
        query = '''
            INSERT INTO mushroom_probabilities (location_id, specie_id, probability, last_updated)
            VALUES (%s, %s, %s, %s)
        '''
        # ON DUPLICATE KEY UPDATE probability=VALUES(probability), last_updated=VALUES(last_updated)
        values = (location_id, specie_id, probability, current_time)
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()  # Ensure the commit is happening
            #print(f"Data inserted/updated successfully for location_id {location_id} and specie_id {specie_id}")
        except Exception as err:  # Catch all exceptions to see if there's any we're missing
            print("Error during database operation:", err)
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()

    def create_elevation_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS elevation_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                latitude FLOAT,
                longitude FLOAT,
                altitude FLOAT
            )
        """)
        self.conn.commit()

    def insert_elevations(self, elevations):
        cursor = self.conn.cursor()
        cursor.executemany("""
            INSERT INTO elevation_data (latitude, longitude, altitude)
            VALUES (%s, %s, %s)
        """, elevations)
        self.conn.commit()

    def drop_mushroom_species_table(self):
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS mushroom_species;')
        self.conn.commit()  # Commit changes after dropping the table
    
    def drop_mushroom_probability_table(self):
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS mushroom_probabilities;')
        self.conn.commit()  # Commit changes after dropping the table

    def insert_forest(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO forest (forest_id, tipo_id, tipo_desc, centroide_lat, centroide_lng, polygon, altitude, location_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', data)
        self.conn.commit()

    def insert_forest_bulk(self, data_tuples, batch_size=1000):
        sql = """
        INSERT INTO forest (forest_id, tipo_id, tipo_desc, centroide_lat, centroide_lng, polygon, altitude, location_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = self.conn.cursor()
        for i in range(0, len(data_tuples), batch_size):
            batch = data_tuples[i:i+batch_size]
            batch = [(forest_id, tipo_id, tipo_desc, centroide_lat, centroide_lng, polygon, altitude, location_id)
                     for (forest_id, tipo_id, tipo_desc, centroide_lat, centroide_lng, polygon, altitude, location_id) in batch]
            cursor.executemany(sql, batch)
            self.conn.commit()
        cursor.close()

    def fetch_elevation_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, latitude, longitude, altitude FROM elevation_data")
        data = cursor.fetchall()
        cursor.close()
        return data

    def fetch_existing_data(self, location_ids, batch_size=1000):
        existing_data = []
        for i in range(0, len(location_ids), batch_size):
            batch_ids = location_ids[i:i+batch_size]
            sql = "SELECT location_id FROM forest WHERE location_id IN (%s)" % ','.join(['%s'] * len(batch_ids))
            cursor = self.conn.cursor()
            cursor.execute(sql, batch_ids)
            results = cursor.fetchall()
            existing_data.extend([row[0] for row in results])
            cursor.close()
        return existing_data
    
    def insert_weather(self, weather_values):
        cursor = self.conn.cursor()
        insert_query = """
        INSERT INTO weather (weather_id, location_id, date, temp_min, temp_max, temp_avg, prec, prec_acc_3_days, prec_acc_7_days, prec_acc_15_days)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            temp_min=VALUES(temp_min),
            temp_max=VALUES(temp_max),
            temp_avg=VALUES(temp_avg),
            prec=VALUES(prec),
            prec_acc_3_days=VALUES(prec_acc_3_days),
            prec_acc_7_days=VALUES(prec_acc_7_days),
            prec_acc_15_days=VALUES(prec_acc_15_days)
        """
        cursor.execute(insert_query, weather_values)
        self.conn.commit()
        cursor.close()
        
    def insert_mushroom_species(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO mushroom_species (specie_id, specie_name, specie_desc, tipo_bosque_id, temp_max, temp_min, prec_acc_min, prec_acc_max, altura_optima_max, altura_optima_min, altura_min)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', data)
        cursor.close()
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
        cursor = self.conn.cursor()
        query = 'SELECT * FROM users WHERE username = %s'
        result = cursor.execute(query, (username,))
        user = result.fetchone()
        return user

    def get_user_pswd(self, username):
        cursor = self.conn.cursor()
        query = 'SELECT username, password FROM users WHERE username = %s'
        cursor.execute(query, (username,))
        usuario = cursor.fetchone()
        cursor.close()
        if usuario:
            return {'username': usuario[0], 'password': usuario[1]}
        else:
            return None

    def close(self):
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