import os
from datetime import datetime

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'system_logs.txt')

class AuditLogger:
    @staticmethod
    def _write_log(message):
        try:
            with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to write log: {e}")
    
    @staticmethod
    def log(user_id, username, action_type, entity_type=None, entity_id=None, details=None, status="SUCCESS"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (
            f"[{timestamp}] "
            f"USER: {username} (id:{user_id}) | "
            f"ACTION: {action_type} | "
            f"STATUS: {status} | "
            f"DETAILS: {details or '-'}"
        )
        AuditLogger._write_log(log_entry)
    
    @staticmethod
    def get_all_logs(limit=500):
        if not os.path.exists(LOG_FILE_PATH):
            return []
        try:
            with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return [line.strip() for line in lines[-limit:]]
        except Exception as e:
            print(f"[WARNING] Failed to read logs: {e}")
            return []
