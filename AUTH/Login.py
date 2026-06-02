import hashlib
from Database.db import get_connection
def login_user(username,password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT password_hash FROM users WHERE login = ?",
        (username,)  # запятая для tuple нкжна, tuple крч это как const в js, типо нельзя менять ну + sql инъекцию убирает 
    )
    
    row = cursor.fetchone()  # берём запись, чтобы дальше ее сравнить
    conn.close()
    
    #if row is None:
     #   return False  # пользователь есть в бд? 
    
    #return row[0] == password_hash  # Ну типа совпал пароль или нет

    if row:
        return row[0]
    return None


    