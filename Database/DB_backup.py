import os
import shutil
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bd.db')
BACKUP_DIR = os.path.join(os.path.dirname(__file__), '..', 'backups')
CHECKSUM_FILE = os.path.join(os.path.dirname(__file__), '..', 'db_checksum.txt')

def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def get_checksum():
    if not os.path.exists(DB_PATH):
        return None
    with open(DB_PATH, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def save_checksum():
    with open(CHECKSUM_FILE, 'w') as f:
        f.write(get_checksum() or "")

def check_integrity():
    if not os.path.exists(CHECKSUM_FILE):
        return True
    with open(CHECKSUM_FILE, 'r') as f:
        saved = f.read().strip()
    return get_checksum() == saved

def create_backup(reason=""):
    ensure_backup_dir()
    if not os.path.exists(DB_PATH):
        return False
    name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{reason}.db"
    shutil.copy2(DB_PATH, os.path.join(BACKUP_DIR, name))
    save_checksum()
    return True

def backup_before_change(reason):
    """Вызывай ЭТУ функцию перед любым изменением БД"""
    return create_backup(reason)
