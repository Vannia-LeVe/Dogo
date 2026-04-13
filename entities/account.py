import pymysql
from persistence.db import get_connection

class Account:
    def __init__(self, id: int, number: str, id_user: int):
        self.id = id
        self.number = number
        self.id_user = id_user
    
    @staticmethod
    def get_by_user_id(id_user: int):
        """Obtiene la cuenta principal de un usuario"""
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            sql = "SELECT id, number, id_user FROM account WHERE id_user = %s "
            cursor.execute(sql, (id_user,))
            
            row = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if row:
                return Account(row["id"], row["number"], row["id_user"])
            return None
        except Exception as ex:
            print(f"Error getting account: {ex}")
            return None