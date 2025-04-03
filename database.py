import os
from mysql.connector import connect, pooling, Error
from dotenv import load_dotenv

# Loads sensitive data from .env
load_dotenv()
SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_USER = os.getenv('SERVER_USER')
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')

# Creates connection pool
def createPool():
    try:
        config = {
            'host' : SERVER_HOST,
            'user' : SERVER_USER,
            'password' : SERVER_PASSWORD,
            'database' : "Uniform_Distribution_DB"
        }
        pool = pooling.MySQLConnectionPool(pool_name = "pool", pool_size = 3, autocommit = True, **config)
        return pool
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Opens a connection to the database, will keep for later evalution test of how pooling effects performance
def openConnection():
    try:
        config = {
            'host' : SERVER_HOST,
            'user' : SERVER_USER,
            'password' : SERVER_PASSWORD,
            'database' : "Uniform_Distribution_DB"
        }
        connection = connect(autocommit = True, **config)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None
    
