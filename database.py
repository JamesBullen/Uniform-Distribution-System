import mysql.connector
import os
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
        pool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "pool", pool_size = 3, autocommit = True, **config)
        return pool
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

# Opens a connection to the database
def openConnection():
    try:
        config = {
            'host' : SERVER_HOST,
            'user' : SERVER_USER,
            'password' : SERVER_PASSWORD,
            'database' : "Uniform_Distribution_DB"
        }
        connection = mysql.connector.connect(autocommit = True, **config)
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None