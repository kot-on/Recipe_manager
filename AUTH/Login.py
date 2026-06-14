import hashlib
from Database.db import get_connection
def login_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE login = ?",
        (username,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    if row and row[1] == password_hash:  # сравниваем хеши
        return row[0]  # возвращаем id, а не хеш
    return None


    