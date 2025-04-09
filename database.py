import os
from mysql.connector import connect, pooling, Error
from dotenv import load_dotenv

# Loads sensitive data from .env
load_dotenv()
SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_USER = os.getenv('SERVER_USER')
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')

tablesDict = {'tbl_roles': None, 'tbl_colours': None, 'tbl_sizes': None}
# Prevents issue of circular importing when needing pool connection from app.py
poolConnection = None

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

        # Keeps a copy of pool connection for itself
        global poolConnection 
        poolConnection = pool

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
def extractTable(table):
    global poolConnection
    try:
        # Connects to pool
        connection = poolConnection.get_connection()
        # Open cursor and runs fetch query
        cursor = connection.cursor()
        query = f"SELECT * FROM {table}" #! Parameterised queries can't be used for identifiers like table names, never use this function for anything with user inputs
        cursor.execute(query)
        result = cursor.fetchall()

        # Close cursor and return connection to pool
        cursor.close()
        connection.close()

        return result
    except Error as e:
        print(f"Query error: {e}")
        return None
    
def loadValidtionTables():
    global tablesDict
    for table in tablesDict:
        tablesDict[table] = extractTable(table)

def getValidtionTable(table):
    global tablesDict
    return tablesDict[table]
    
def callProcedure(query, args):
    global poolConnection
    try:
        # Connect to pool
        #connection = poolConnection.get_connection()
        connection = openConnection()
        # Open cursor and runs fetch query
        cursor = connection.cursor()
        if not args:
            cursor.execute(query)
        else:
            cursor.execute(query, args if isinstance(args, list) else (args,))
        result = cursor.fetchall()
        
        # Gets headers for columns
        headers = []
        if cursor.description:
            headers = [i[0] for i in cursor.description]
        
        # Close cursor and return connection to pool
        cursor.close()
        connection.close()
        
        return result, headers
    except Error as e:
        print(f"Error: {e}")
        return