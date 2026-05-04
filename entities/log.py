
from datetime import datetime

import pymysql
from enums.log_type import LogType
from entities.user import User
from persistence.db import get_connection
# Historial de acciones que ha realizado el usuario para que no pueda negarlas y haya una disputa 
class Log:
    def __init__(self, id:int, date:datetime, user:User,
                 description: str, type: LogType  ):
        
        self.id= id,
        self.date= date
        self.user= user
        self.description= description
        self.type= type
    
    
    
    def save_log(user: User, description: str, type: LogType):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            sql = "INSERT INTO log (id_user, date, description, type) VALUES (%s, NOW(), %s, %s)"
            cursor.execute(sql, (user.id, description, type.value))

            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Error al guardar el log: {e}")
            return False
        
   
    def get_all_logs():
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM log ORDER BY date DESC"
            cursor.execute(sql)
            logs = cursor.fetchall()
            cursor.close()
            connection.close()
            return logs
        except Exception as ex:
            print(f"Error: {ex}")
            return []