import pymysql
from entities.permission import Permission
from enums.profile_type import ProfileType
from persistence.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id: int, name: str, email: str, password: str, profile:ProfileType, permissions: list, is_active :bool):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile
        self.permissions=permissions
        self.active= is_active  
    
    def is_active(self):
        return self.active
    def is_admin(self):
        return self.profile==ProfileType.ADMIN
    
    def has_permission(self, permission_value):
        # Si es admin, tiene todos los permisos
        if self.is_admin():
            return True
        # Verificar su lista de permisos
        for perm in self.permissions:
            if perm.value == permission_value:
                return True
        return False
        
    
    def check_email_exists(email) -> bool:
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT email from user WHERE email = %s"
        cursor.execute(sql, (email,))

        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row is not None
    
        
    def save(name: str, email:str, password:str) -> bool:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            hash_password = generate_password_hash(password)

            sql = "INSERT INTO user (name, email, password, profile, is_active) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, email, hash_password, 2, True))
            connection.commit()

            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error saving user:{ex}")
            return False
        
    def check_login(email, password):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            sql = "SELECT id, name, email, password, profile, is_active FROM user WHERE email = %s"
            cursor.execute(sql, (email,))

            user = cursor.fetchone()
            
            cursor.close()
            connection.close()

            if user and check_password_hash(user['password'], password):
                permissions = Permission.get_permission_by_user(user["id"])
                profile_type = ProfileType(int(user["profile"]))
                
                # CORRECCIÓN: Definir is_active con un valor por defecto
                is_active = False  # Valor por defecto
                if user["is_active"] is not None:
                    if isinstance(user["is_active"], bytes):
                        is_active = user["is_active"] == b'\x01'
                    elif isinstance(user["is_active"], bool):
                        is_active = user["is_active"]
                    else:
                        is_active = bool(user["is_active"])
                
                # CORRECCIÓN: Crear el objeto User fuera del bloque if
                return User(
                    user["id"],
                    user["name"],
                    user["email"],
                    user["password"],
                    profile_type,
                    permissions,
                    is_active
                )

            return None
        except Exception as ex:
            print(f"Error login user:{ex}")
            return None
        
    def get_by_id(id):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            # CORRECCIÓN: Agregar profile e is_active a la consulta SQL
            sql = "SELECT id, name, email, password, profile, is_active FROM user WHERE id = %s"
            cursor.execute(sql, (id,))

            user = cursor.fetchone()
            
            cursor.close()
            connection.close()

            if user:
                profile = ProfileType(int(user["profile"]))
                permission = Permission.get_permission_by_user(user["id"])

                # CORRECCIÓN: Definir is_active con un valor por defecto
                is_active = False  # Valor por defecto
                if user["is_active"] is not None:
                    if isinstance(user["is_active"], bytes):
                        is_active = user["is_active"] == b'\x01'
                    elif isinstance(user["is_active"], bool):
                        is_active = user["is_active"]
                    else:
                        is_active = bool(user["is_active"])
                
                return User(
                    user["id"],
                    user["name"],
                    user["email"],
                    user["password"],
                    profile,
                    permission,
                    is_active
                )

            return None
        except Exception as ex:
            print(f"Error login user:{ex}")
            return None
    
