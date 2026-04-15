import pymysql
from entities.transaction import Transaction
from entities.user import User
from persistence.db import get_connection
from datetime import datetime

class Account:
    def __init__(self, id: int, number: str,creation_date:datetime, user: User,transactions: list): # en id_user en la tabla esta como FK 
        self.id = id
        self.number = number
        self.creation_date=creation_date
        self.user=user
        self.transactions=transactions
        
    
   
    def get_account_by_id(id_user: int):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            sql = "SELECT id, number,creation_date, id_user FROM account WHERE id_user = %s "
            cursor.execute(sql, (id_user,))
            
            rs = cursor.fetchone()
            user= User.get_by_id(rs["id_user"])
            
            transactions=Transaction.get_transaction_by_account(rs["id_account"])
            
            account=Account(
                rs["id"],
                rs["number"],
                rs["creation_date"],
                user,
                transactions
            )
            cursor.close()
            connection.close()
            return account
        
        except Exception as ex:
            print(f"Error getting account: {ex}")
            return None