import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",  
            password="root@39",  
            database="inventorysales"  
        )

        if connection.is_connected():
            print("Database connection successful.")
            return connection

    except Error as e:
        print("Error while connecting to database:", e)
        return None
