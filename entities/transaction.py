import pymysql
from enums.transaction_type import TransactionTyoe
from datetime import datetime
from persistence.db import get_connection

class Transaction:
    def __init__(self, amount: float, description: str, date:datetime,type:TransactionTyoe):
        self.amount = amount
        self.type = type
        self.description = description
        self.date = date
    
    def get_transaction_by_account(id_account: int):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT amount, description, date, type FROM transaction WHERE id_account = %s "
            cursor.execute(sql, (id_account,)) 
            
            rs = cursor.fetchall()

            transactions=Transaction(rs["amount"],rs["description"],rs["date"],rs["type"])
            transactions.append(transactions)
            
            cursor.close()
            connection.close()
            return transactions
            
        except Exception as ex:
            print(f"Error getting transactions: {ex}")
            return None
