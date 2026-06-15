import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), 'UI_logs.txt')

def log_ui_action(username: str, button_name: str):
    """Записывает нажатие кнопки в лог-файл"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] | Пользователь: {username:<20} | Кнопка: {button_name}\n"
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line)
    except Exception as e:
        print(f"[WARNING] Не удалось записать UI лог: {e}")