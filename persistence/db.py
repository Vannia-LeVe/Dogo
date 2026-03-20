
import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3307,
        user="root",
        password="admin",
        database="dogo_db")
   