import mysql.connector
import os
from dotenv import load_dotenv

# Loads sensitive data from .env
load_dotenv()
SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_USER = os.getenv('SERVER_USER')
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')

# Opens a connection to the database
def open_connection():
    try:
        connection = mysql.connector.connect(
            host = SERVER_HOST,
            user = SERVER_USER,
            password = SERVER_PASSWORD,
            database = "Uniform_Distribution_DB"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None