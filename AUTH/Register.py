import hashlib
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Database.db import get_connection
from Logger_logic import AuditLogger

def register_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Проверка: существует ли уже такой пользователь
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return None
    
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password_hash)
    )
    conn.commit()
    user_id = cursor.lastrowid
    
    # Логируем регистрацию
    AuditLogger.log(user_id, username, "REGISTER", entity_type="USER", entity_id=user_id, details=f"Регистрация пользователя {username}", status="SUCCESS")
    
    conn.close()
    return user_id
