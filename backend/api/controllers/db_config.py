from mysql.connector import pooling

# db_config.py
mysql_params = {
    "host": "database-forest.c1qoas008ih1.eu-north-1.rds.amazonaws.com ",
    "port": 3306,
    "user": "admin",
    "password": "chetler2",
    "database": "forest-RDS"
}


mysql_params_old = {
    "host": "localhost",
    "port": 3306,
    "user": "mario",
    "password": "chetler2",
    "database": "forest"
}

# Configurar el pool de conexiones
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,  # Ajusta el tamaño del pool según tus necesidades
    **mysql_params
)