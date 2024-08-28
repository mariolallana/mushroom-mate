import mysql.connector
import pandas as pd
from tabulate import tabulate

class ForestModel:
    def __init__(self, mysql_params, connection=None):
        """Initialize the ForestModel with database connection."""
        if connection:
            self.conn = connection
        else:
            self.conn = mysql.connector.connect(**mysql_params)
        self.cursor = self.conn.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # Database utility methods
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.conn.commit()
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            self.conn.rollback()
            raise

    # Table creation methods
    def create_tables(self):
        """Create all necessary tables if they don't exist."""
        self.create_forest()
        self.create_forest_aux()
        self.create_weather()
        self.create_elevation_table()
        self.create_users_table()
        self.create_mushroom_species_table()
        self.create_mushroom_probabilities_table()

    def create_forest(self):
        """Create the main forest table."""
        query = '''
        CREATE TABLE IF NOT EXISTS forest (
            location_id VARCHAR(255) PRIMARY KEY,
            tipo_id INTEGER,
            tipo_desc TEXT,
            centroide_lat FLOAT,
            centroide_lng FLOAT,
            polygon LONGBLOB,
            altitude FLOAT
        );
        '''
        self.execute_query(query)

    def create_forest_aux(self):
        """Create the auxiliary forest table."""
        query = '''
        CREATE TABLE IF NOT EXISTS forest_aux (
            location_id VARCHAR(255) PRIMARY KEY,
            tipo_id INTEGER,
            tipo_desc TEXT,
            centroide_lat_wgs84 FLOAT,
            centroide_lng_wgs84 FLOAT,
            polygon LONGTEXT
        );
        '''
        self.execute_query(query)

    def create_weather(self):
        """Create the weather table."""
        query = '''
        CREATE TABLE IF NOT EXISTS weather (
            weather_id VARCHAR(255) PRIMARY KEY,
            location_id VARCHAR(255),
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
        '''
        self.execute_query(query)

    def create_elevation_table(self):
        """Create the elevation data table."""
        query = '''
        CREATE TABLE IF NOT EXISTS elevation_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            latitude FLOAT,
            longitude FLOAT,
            altitude FLOAT
        );
        '''
        self.execute_query(query)

    def create_mushroom_species_table(self):
        """Create the mushroom_species table."""
        query = '''
        CREATE TABLE IF NOT EXISTS mushroom_species (
            specie_id INT PRIMARY KEY,
            specie_name VARCHAR(255),
            specie_desc TEXT,
            tipo_bosque_id INT,
            temp_max FLOAT,
            temp_min FLOAT,
            prec_acc_min FLOAT,
            prec_acc_max FLOAT,
            altura_optima_max INT,
            altura_optima_min INT,
            altura_max INT,
            culinary_value INT,
            appreciation_desc TEXT
        );
        '''
        self.execute_query(query)

    def create_mushroom_probabilities_table(self):
        """Create the mushroom_probabilities table."""
        query = '''
        CREATE TABLE IF NOT EXISTS mushroom_probabilities (
            location_id VARCHAR(255),
            specie_id INT,
            probability FLOAT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (location_id, specie_id),
            FOREIGN KEY (location_id) REFERENCES forest(location_id),
            FOREIGN KEY (specie_id) REFERENCES mushroom_species(specie_id)
        );
        '''
        self.execute_query(query)

    def create_users_table(self):
        """Create the users table."""
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        );
        '''
        self.execute_query(query)

    # Data insertion methods
    def insert_forest(self, data):
        """Insert a single forest record."""
        query = '''
        INSERT INTO forest (location_id, tipo_id, tipo_desc, centroide_lat, centroide_lng, polygon, altitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        self.execute_query(query, data)

    def insert_forest_bulk(self, data_tuples, batch_size=1000):
        """Insert multiple forest records in bulk."""
        query = '''
        INSERT INTO forest (location_id, tipo_id, tipo_desc, centroide_lat, centroide_lng, polygon, altitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        cursor = self.conn.cursor()
        try:
            for i in range(0, len(data_tuples), batch_size):
                batch = data_tuples[i:i+batch_size]
                cursor.executemany(query, batch)
                self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")
            print(f"Sample data tuple: {batch[0] if batch else 'No data'}")
            print(f"Number of fields in data tuple: {len(batch[0]) if batch else 0}")
            self.conn.rollback()
        finally:
            cursor.close()

    def insert_forest_aux_bulk(self, data_tuples, batch_size=1000):
        """Insert multiple auxiliary forest records in bulk."""
        query = '''
        INSERT INTO forest_aux (tipo_id, tipo_desc, centroide_lat_wgs84, centroide_lng_wgs84, polygon, location_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor = self.conn.cursor()
        try:
            for i in range(0, len(data_tuples), batch_size):
                batch = data_tuples[i:i+batch_size]
                cursor.executemany(query, batch)
                self.conn.commit()
        except mysql.connector.Error as err:
            print("Error inserting data:", err)
            self.conn.rollback()
        finally:
            cursor.close()

    def insert_weather(self, weather_values):
        """Insert or update a weather record."""
        query = '''
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
        '''
        self.execute_query(query, weather_values)

    def insert_weather_bulk(self, weather_values_list):
        """Insert or update multiple weather records."""
        query = '''
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
        '''
        cursor = self.conn.cursor()
        try:
            cursor.executemany(query, weather_values_list)
            self.conn.commit()
        except mysql.connector.Error as err:
            self.conn.rollback()
            raise err
        finally:
            cursor.close()

    def insert_elevations(self, elevations):
        """Insert multiple elevation records."""
        query = "INSERT INTO elevation_data (latitude, longitude, altitude) VALUES (%s, %s, %s)"
        cursor = self.conn.cursor()
        cursor.executemany(query, elevations)
        self.conn.commit()

    def insert_mushroom_species(self, data):
        """Insert a single mushroom species record."""
        query = '''
        INSERT INTO mushroom_species (specie_id, specie_name, specie_desc, tipo_bosque_id, temp_max, temp_min, 
                                    prec_acc_min, prec_acc_max, altura_optima_max, altura_optima_min, altura_max,
                                    culinary_value, appreciation_desc)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.execute_query(query, data)

    def update_probability_record(self, location_id, specie_id, probability):
        query = '''
        INSERT INTO mushroom_probabilities (location_id, specie_id, probability)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        probability = VALUES(probability),
        last_updated = CURRENT_TIMESTAMP
        '''
        self.execute_query(query, (location_id, specie_id, probability))

    def batch_update_probability_records(self, records):
        """Batch update or insert probability records."""
        query = '''
        INSERT INTO mushroom_probabilities (location_id, specie_id, probability)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        probability = VALUES(probability),
        last_updated = CURRENT_TIMESTAMP
        '''
        with self.conn.cursor() as cursor:
            cursor.executemany(query, records)
        self.conn.commit()

    def insert_user(self, username, password):
        """Insert a new user."""
        query = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        self.execute_query(query, (username, password))

    # Data retrieval methods
    def fetch_aux_data(self):
        """Fetch all data from the auxiliary forest table."""
        query = "SELECT tipo_id, tipo_desc, centroide_lat_wgs84, centroide_lng_wgs84, polygon, location_id FROM forest_aux"
        result = self.execute_query(query)
        return pd.DataFrame(result) if result else pd.DataFrame()

    def get_existing_elevation_coordinates(self):
        """Get existing elevation coordinates."""
        query = "SELECT latitude, longitude FROM elevation_data"
        result = self.execute_query(query)
        return [(row['latitude'], row['longitude']) for row in result]

    def fetch_elevation_data(self):
        """Fetch all elevation data."""
        query = "SELECT id, latitude, longitude, altitude FROM elevation_data"
        return self.execute_query(query)

    def fetch_existing_data(self, location_ids):
        """Fetch existing forest data for given location IDs."""
        format_strings = ','.join(['%s'] * len(location_ids))
        query = f"SELECT location_id FROM forest WHERE location_id IN ({format_strings})"
        result = self.execute_query(query, tuple(location_ids))
        return [item['location_id'] for item in result]

    def fetch_mushroom_species(self):
        """Fetch all mushroom species."""
        query = "SELECT specie_id, specie_name FROM mushroom_species ORDER BY specie_id"
        return self.execute_query(query)
    
    def fetch_mushroom_species_by_id(self, specie_id):
        """Fetch a single mushroom species by its ID."""
        query = "SELECT * FROM mushroom_species WHERE specie_id = %s"
        result = self.execute_query(query, (specie_id,))
        return result[0] if result else None
    
    def fetch_all_mushroom_species(self):
        """Fetch all data from the mushroom_species table."""
        query = "SELECT * FROM mushroom_species"
        return self.execute_query(query)

    def get_user_pswd(self, username):
        """Get user password for given username."""
        query = 'SELECT username, password FROM users WHERE username = %s'
        result = self.execute_query(query, (username,))
        return result[0] if result else None

    # Utility methods
    def drop_mushroom_species_table(self):
        """Drop the mushroom_species table if it exists."""
        query = 'DROP TABLE IF EXISTS mushroom_species;'
        self.execute_query(query)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
# Example usage (commented out)
'''
if __name__ == "__main__":
    from db_config import mysql_params
    forest_model = ForestModel(mysql_params)
    forest_model.create_tables()
    # Add more example usage as needed
    forest_model.close()
'''