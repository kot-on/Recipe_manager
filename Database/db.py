import sqlite3
import os

# Путь к бд, чтобы не писать его везде
# Семен тебе нужно будет работать с шифрованием этого канала подключения к бд
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bd.db')

def get_connection():
    return sqlite3.connect(DB_PATH)