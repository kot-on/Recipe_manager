import sqlite3
import os
from Logger_logic import AuditLogger
# Путь к бд, чтобы не писать его везде
# Семен тебе нужно будет работать с шифрованием этого канала подключения к бд
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bd.db')

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
        ingredients = cursor.fetchall()  # список кортежей ("мука", "200", "г")

        result.append({
            "id": recipe_id,
            "title": title,
            "description": description,
            "rating": rating,
            "image_path": image_path,
            "ingredients": ingredients
        })

    conn.close()
    return result

def save_recipe(user_id, title, description, rating, image_path, ingredients):
    conn = get_connection()
    cursor = conn.cursor()

    # Сохраняем рецепт
    cursor.execute(
        "INSERT INTO recipes (user_id, title, description, rating, image_path) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, description, rating, image_path)
    )
    recipe_id = cursor.lastrowid  # id только что созданного рецепта

    # Сохраняем каждый ингредиент
    for name, amount, unit in ingredients:
        cursor.execute(
            "INSERT INTO ingredients (recipe_id, name, amount, unit) VALUES (?, ?, ?, ?)",
            (recipe_id, name, amount, unit)
        )

    conn.commit()
    conn.close()
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
    return result
