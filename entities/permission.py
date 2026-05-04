#lista de permisoso 
import pymysql

from enums.Valuepermission import ValuePermission
from persistence.db import get_connection


class Permission(): #se esta heredando
    def __init__(self, id: int, value:ValuePermission):
        self.id = id
        self.value= value 
        
    def get_permission_by_user(id_user):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT id, value, id_user FROM permission WHERE id_user = %s "
            cursor.execute(sql, (id_user,)) 
            
            
            rs = cursor.fetchall()
            permissions = []
            for row in rs:
                 permissions.append(Permission(row["id"],
                ValuePermission(row["value"])))
            
               
            cursor.close()
            connection.close()
            return permissions
            
        except Exception as ex:
            print(f"Error con los permisos: {ex}")
            return [] 
        
    @staticmethod
    def assign_permission(id_user, value_permission):
    
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            # Primero verificar si ya tiene ese permiso
            sql_check = "SELECT id FROM permission WHERE id_user = %s AND value = %s"
            cursor.execute(sql_check, (id_user, value_permission))
            if cursor.fetchone():
                return True  # Ya tiene el permiso
            
            # Si no lo tiene, asignarlo
            sql = "INSERT INTO permission (id_user, value) VALUES (%s, %s)"
            cursor.execute(sql, (id_user, value_permission))
            connection.commit()
            
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error assigning permission: {ex}")
            return False