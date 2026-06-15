import sqlite3
import os

# Путь к бд, чтобы не писать его везде
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bd.db')

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
    return sqlite3.connect(DB_PATH)

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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
    log_db(f"DELETE рецепт recipe_id={recipe_id}")

def update_recipe(recipe_id, title, description, rating, image_path, ingredients):
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