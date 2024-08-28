import mysql.connector
from mysql.connector import pooling
import sqlalchemy
from api.controllers.db_config import mysql_params

connection_pool = None

def initialize_connection_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=20,
            pool_reset_session=True,
            **mysql_params
        )

def get_connection():
    initialize_connection_pool()
    return connection_pool.get_connection()

def get_sqlalchemy_engine():
    connection_string = f"mysql+mysqlconnector://{mysql_params['user']}:{mysql_params['password']}@{mysql_params['host']}:{mysql_params['port']}/{mysql_params['database']}"
    return sqlalchemy.create_engine(connection_string, pool_size=20, max_overflow=0)

def close_connection(connection):
    if connection.is_connected():
        connection.close()