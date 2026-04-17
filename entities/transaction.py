import pymysql
from enums.transaction_type import TransactionType
from datetime import datetime
from persistence.db import get_connection

class Transaction:
    def __init__(self, id:int ,date:datetime  , description: str, amount: float ,type:TransactionType):
        self.id = id
        self.amount = amount
        self.type = type
        self.description = description
        self.date = date
    
    def get_transaction_by_account(id_account: int):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT id, amount , description,date, type FROM transaction WHERE id_account = %s "
            cursor.execute(sql, (id_account,)) 
            
            
            rs = cursor.fetchall()
            transactions = []
            for row in rs:

                transaction_Type = TransactionType(row["type"])
              
                transaction = Transaction(
                    row["id"],
                    row["date"],
                    row["description"],
                    row["amount"],
                    transaction_Type
                )
                transactions.append(transaction)
            
            cursor.close()
            connection.close()
            return transactions
            
        except Exception as ex:
            print(f"Error con las transacciones: {ex}")
            return [] 
