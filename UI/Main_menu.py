import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tkinter import *
import customtkinter
from Database.db import show_3_recipes
from PIL import Image, ImageTk
from Recipe_manage import open_recipe_manager
from Recipe_view import open_all_recipes
from UI_logger import log_ui_action

def open_main_window(User_id, username=None):
    root = Tk()
    root.title("Recipe Manager")
    root.geometry("1600x900")
    root.configure(bg='Black')

    pil_image = Image.open("Assets/Logo.png")
    img_logo = ImageTk.PhotoImage(pil_image)
    logo_label = Label(root, image=img_logo, bg='Black')
    logo_label.image = img_logo 
    logo_label.pack(pady=(20, 5))
    Label(root, text="Recipe manager", fg='#585B91', font=('Inter', 50), bg='Black').pack()

    customtkinter.CTkButton(root, width=600, height=60, corner_radius=15, font=('Inter', 20), text='Добавить рецепт', fg_color="#F54927", command=lambda: [log_ui_action(username, "Добавить рецепт"), root.withdraw(),open_recipe_manager(root, User_id, username, on_save=refresh)]).pack(pady=15)

    recipes_frame = Frame(root, bg='Black')
    recipes_frame.pack(fill=BOTH, expand=True)

    load_recipes(User_id, recipes_frame)

    def refresh():
        # Очищаем фрейм с рецептами
        for widget in recipes_frame.winfo_children():
            widget.destroy()
        # Загружаем заново
        load_recipes(User_id, recipes_frame)

    customtkinter.CTkButton(root, text="Показать все рецепты", width=200, height=23,fg_color='black', font=('Inter', 15, "underline"), corner_radius=10,text_color='#63078E', command=lambda: [log_ui_action(username, "Показать все рецепты"),root.withdraw(),open_all_recipes(root, User_id,username,on_main_refresh=refresh)]).pack(pady=10)
    
    root.mainloop()

def load_recipes(User_id, frame):
    recipes = show_3_recipes(User_id)

    if not recipes:
        Label(
            frame,
            text="У вас пока нет рецептов\nНажмите «Добавить» чтобы создать первый!",
            font=('Inter', 16),
            fg="gray",
            bg="Black"
        ).pack(expand=True)
        return

    for recipe in recipes:
        card = Frame(frame, bg="#1E1E1E", pady=10)
        card.pack(fill=X, padx=20, pady=10)

        # Картинка слева
        try:
            img = Image.open(recipe["image_path"]).resize((150, 150))
            photo = ImageTk.PhotoImage(img)
        except:
            img = Image.open("Assets/default.png").resize((150, 150))
            photo = ImageTk.PhotoImage(img)

        img_label = Label(card, image=photo, bg="#1E1E1E")
        img_label.image = photo
        img_label.pack(side=LEFT, padx=15)

        # Текст справа
        text_frame = Frame(card, bg="#1E1E1E")
        text_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        Label(text_frame, text=recipe["title"], font=('Inter', 20, 'bold'),
              bg="#1E1E1E", fg="white", anchor="w").pack(anchor="w")

        Label(text_frame, text=f"⭐ Рейтинг: {recipe['rating']}",
              font=('Inter', 14), bg="#1E1E1E", fg="#FFD700").pack(anchor="w", pady=4)

        Label(text_frame, text=recipe["description"], font=('Inter', 13),
              bg="#1E1E1E", fg="#CCCCCC", wraplength=700,
              justify=LEFT).pack(anchor="w")

        # Ингредиенты
        if recipe["ingredients"]:
            ing_text = "  •  ".join([f"{name} {amount}{unit}"
                                     for name, amount, unit in recipe["ingredients"]])
            Label(text_frame, text=f" {ing_text}", font=('Inter', 12),
                  bg="#1E1E1E", fg="#AAAAAA", wraplength=700,
                  justify=LEFT).pack(anchor="w", pady=(4, 0))
