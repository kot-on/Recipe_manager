import sys
import os
import sqlite3
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

DB_PATH = os.path.join(os.path.dirname(__file__), 'Database', 'recipes.db')

class AuditLogger:
    """Подсистема аудита для защиты и логирования действий"""
    
    @staticmethod
    def ensure_logs_table():
        """Гарантирует существование таблицы Logs в БД"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id INTEGER,
                username TEXT,
                action_type TEXT NOT NULL,
                entity_type TEXT,
                entity_id INTEGER,
                details TEXT,
                status TEXT DEFAULT 'SUCCESS'
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_user ON Logs(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_time ON Logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_action ON Logs(action_type)')
        conn.commit()
        conn.close()
    
    @staticmethod
    def log(user_id, username, action_type, entity_type=None, entity_id=None, details=None, status="SUCCESS"):
        """Запись события в лог"""
        try:
            AuditLogger.ensure_logs_table()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            timestamp = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO Logs (timestamp, user_id, username, action_type, entity_type, entity_id, details, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, user_id, username, action_type, entity_type, entity_id, details, status))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[WARNING] Failed to write log: {e}")
    
    @staticmethod
    def get_user_logs(user_id, limit=100):
        """Получить последние логи пользователя"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, action_type, entity_type, details, status
            FROM Logs
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        logs = cursor.fetchall()
        conn.close()
        return logs
    
    @staticmethod
    def get_all_logs(limit=500):
        """Получить последние логи системы"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, username, action_type, entity_type, details, status
            FROM Logs
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        logs = cursor.fetchall()
        conn.close()
        return logs



