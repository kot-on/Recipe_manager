import sqlite3
import os
import shutil
# Путь к бд, чтобы не писать его везде
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bd.db')
BACKUP_DIR = os.path.join(os.path.dirname(__file__), '..', 'backbd')
BACKUP_PATH = os.path.join(BACKUP_DIR, 'bd_backup.db')
DB_PASSWORD = "K#9mX$vL2@pQ8nR!"

def create_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    shutil.copy2(DB_PATH, BACKUP_PATH)

def restore_from_backup():
    if os.path.exists(BACKUP_PATH):
        shutil.copy2(BACKUP_PATH, DB_PATH)
        print("БД восстановлена из бэкапа")
    else:
        raise RuntimeError("Бэкап не найден, восстановление невозможно")

def log_db(message: str):
    """Записывает сообщение в таблицу Logs"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Logs (log_message) VALUES (?)",
            (message,)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[WARNING] Не удалось записать DB лог: {e}")

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(f"PRAGMA key='{DB_PASSWORD}';")
        conn.execute("SELECT count(*) FROM sqlite_master;")
        return conn
    except Exception:
        print("Основная БД повреждена, восстанавливаем из бэкапа...")
        restore_from_backup()
        conn = sqlite3.connect(DB_PATH)
        conn.execute(f"PRAGMA key='{DB_PASSWORD}';")
        conn.execute("SELECT count(*) FROM sqlite_master;")
        return conn

def show_3_recipes(User_id, limit=3):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, description, rating, image_path FROM recipes WHERE user_id = ? LIMIT ?",
        (User_id, limit)
    )
    recipes = cursor.fetchall()

    result = []
    for row in recipes:
        recipe_id, title, description, rating, image_path = row

        cursor.execute(
            "SELECT name, amount, unit FROM ingredients WHERE recipe_id = ?",
            (recipe_id,)
        )
        ingredients = cursor.fetchall()

        result.append({
            "id": recipe_id,
            "title": title,
            "description": description,
            "rating": rating,
            "image_path": image_path,
            "ingredients": ingredients
        })

    conn.close()
    log_db(f"SELECT 3 рецепта для user_id={User_id}, получено: {len(result)}")
    return result

def save_recipe(user_id, title, description, rating, image_path, ingredients):
    create_backup()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO recipes (user_id, title, description, rating, image_path) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, description, rating, image_path)
    )
    recipe_id = cursor.lastrowid

    for name, amount, unit in ingredients:
        cursor.execute(
            "INSERT INTO ingredients (recipe_id, name, amount, unit) VALUES (?, ?, ?, ?)",
            (recipe_id, name, amount, unit)
        )

    conn.commit()
    conn.close()
    log_db(f"INSERT рецепт '{title}' для user_id={user_id}, recipe_id={recipe_id}, ингредиентов: {len(ingredients)}")
    return recipe_id

def get_all_recipes(User_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, description, rating, image_path FROM recipes WHERE user_id = ?",
        (User_id,)
    )
    recipes = cursor.fetchall()

    result = []
    for row in recipes:
        recipe_id, title, description, rating, image_path = row

        cursor.execute(
            "SELECT name, amount, unit FROM ingredients WHERE recipe_id = ?",
            (recipe_id,)
        )
        ingredients = cursor.fetchall()

        result.append({
            "id": recipe_id,
            "title": title,
            "description": description,
            "rating": rating,
            "image_path": image_path,
            "ingredients": ingredients
        })

    conn.close()
    log_db(f"SELECT все рецепты для user_id={User_id}, получено: {len(result)}")
    return result

def delete_recipe(recipe_id):
    create_backup()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
    log_db(f"DELETE рецепт recipe_id={recipe_id}")

def update_recipe(recipe_id, title, description, rating, image_path, ingredients):
    create_backup() 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE recipes SET title=?, description=?, rating=?, image_path=? WHERE id=?",
        (title, description, rating, image_path, recipe_id)
    )
    cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
    for name, amount, unit in ingredients:
        cursor.execute(
            "INSERT INTO ingredients (recipe_id, name, amount, unit) VALUES (?, ?, ?, ?)",
            (recipe_id, name, amount, unit)
        )
    conn.commit()
    conn.close()
    log_db(f"UPDATE рецепт recipe_id={recipe_id}, новое название='{title}'")