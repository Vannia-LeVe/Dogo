import pymysql
from persistence.db import get_connection

class Transaction:
    def __init__(self, amount: float, type: int, description: str, date, id_account: int):
        self.amount = amount
        self.type = type
        self.description = description
        self.date = date
        self.id_account= id_account
    
    @staticmethod
    def get_by_account_id(id_account: int):
        """Obtiene las transacciones de una cuenta"""
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            sql = """SELECT id, amount, type, description, date, id_account
                     FROM transaction 
                     WHERE id_account = %s 
                     ORDER BY date DESC """
            cursor.execute(sql, (id_account))
            
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            
            transactions = []
            for row in rows:
                transactions.append(Transaction(
                    row["amount"], row["type"], row["description"], 
                    row["date"], row["id_account"]
                ))
            return transactions
        except Exception as ex:
            print(f"Error con las transacciones : {ex}")
            return []