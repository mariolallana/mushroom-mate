import sqlite3
import pandas as pd

def get_all_tables(conn):
    """
    Función para obtener todos los nombres de las tablas en la base de datos SQLite.
    """
    # Consulta para obtener los nombres de todas las tablas en la base de datos
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Extraer los nombres de las tablas de la consulta
    tables = cursor.fetchall()
    
    # Cerrar el cursor
    cursor.close()
    
    return [table[0] for table in tables]

def main():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('weather_data.db')
    
    # Obtener los nombres de todas las tablas
    tables = get_all_tables(conn)
    
    # Crear un DataFrame para cada tabla y mostrarlo
    for table in tables:
        query = f"SELECT * FROM {table};"
        df = pd.read_sql(query, conn)
        print(f"\nTabla: {table}")
        print(df)
    
    # Cerrar la conexión a la base de datos
    conn.close()

if __name__ == "__main__":
    main()
