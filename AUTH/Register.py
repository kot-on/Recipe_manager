import hashlib
from Database.db import get_connection

def register_user(username,password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "Insert into users (login, password_hash) Values (?,?)",
        (username, password_hash)  # тут sql инъекция + наши переменные передаем в бд
    )
    conn.commit() #Твое любимое Слав, нужно, чтобы сохранять изменения в бд 
    user_id = cursor.lastrowid  # id только что созданного пользователя
    conn.close()
    return user_id