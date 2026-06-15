import hashlib
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Database.db import get_connection
from Core_logic.Logger_logic import AuditLogger

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
    
    if row and row[1] == password_hash:
        # Логируем успешный вход
        AuditLogger.log(row[0], username, "LOGIN", entity_type="USER", entity_id=row[0], details="Успешный вход", status="SUCCESS")
        return row[0]
    else:
        # Логируем неудачную попытку
        AuditLogger.log(None, username, "LOGIN", entity_type="USER", details="Неверный логин или пароль", status="FAILURE")
        return None

    
