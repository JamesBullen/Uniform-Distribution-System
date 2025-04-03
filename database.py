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
    
# Gets all data from a table, to be used extract validation tables that may be updated for dropdowns
# Parameterised queries can't be used for identifiers like table names, never use this function for anything with user inputs
def extractTable(pool, table):
    try:
        # Connects to pool
        connection = pool.get_connection()
        # Open cursor and runs fetch query
        cursor = connection.cursor()
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        result = cursor.fetchall()

        # Gets headers for columns
        headers = [i[0] for i in cursor.description]

        # Close cursor and return connection to pool
        cursor.close()
        connection.close()

        return result, headers
    except Error as e:
        print(f"Database connection error: {e}")
        return None