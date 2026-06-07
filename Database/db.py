import sqlite3
import os
import getpass  

# Путь к БД
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bd.db')


def get_connection():
    password = os.getenv("DB_PASSWORD")

    if not password:
        raise RuntimeError("DB_PASSWORD не задана в переменных окружения")

    user_input = getpass.getpass("Введите пароль для доступа к базе: ")

    if user_input != password:
        raise PermissionError("Неверный пароль. Доступ запрещён.")

    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"PRAGMA key='{password}';")
    conn.execute("SELECT count(*) FROM sqlite_master;")

    return conn


def show_3_recipes(User_id, limit=3):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title, description, rating, image_path
        FROM Recipes
        WHERE User_id = ?
        LIMIT ?
        """,
        (User_id, limit)
    )

    recipes = cursor.fetchall()
    conn.close()

    return recipes


if __name__ == "__main__":
    try:
        conn = get_connection()
        print("База успешно открыта!")

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())

        conn.close()
    except PermissionError as e:
        print(f"Ошибка доступа: {e}")