import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tkinter import *
from Database.db import get_all_recipes
from PIL import Image, ImageTk

def open_all_recipes(root_parent, User_id):
    root = Toplevel(root_parent)
    root.title("Все рецепты")
    root.geometry("1200x800")
    root.configure(bg='Black')

    # --- Логотип ---
    pil_image = Image.open("Assets/Logo.png")
    img_logo = ImageTk.PhotoImage(pil_image)
    logo_label = Label(root, image=img_logo, bg='Black')
    logo_label.image = img_logo
    logo_label.pack(pady=(20, 5))

    Label(root, text="Мои рецепты", fg='#585B91',
          font=('Inter', 40), bg='Black').pack(pady=(0, 10))

    # --- Скролл ---
    canvas = Canvas(root, bg='Black', highlightthickness=0)
    scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    inner_frame = Frame(canvas, bg='Black')
    canvas_window = canvas.create_window((0, 0), window=inner_frame, anchor="n")

    def on_canvas_resize(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", on_canvas_resize)

    def on_frame_resize(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_frame_resize)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # --- Рецепты ---
    load_all_recipes(User_id, inner_frame)


def load_all_recipes(User_id, frame):
    recipes = get_all_recipes(User_id)

    if not recipes:
        Label(
            frame,
            text="У вас пока нет рецептов\nНажмите «Добавить» чтобы создать первый!",
            font=('Inter', 16),
            fg="gray",
            bg="Black"
        ).pack(expand=True, pady=50)
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

        if recipe["ingredients"]:
            ing_text = "  •  ".join([f"{name} {amount}{unit}"
                                     for name, amount, unit in recipe["ingredients"]])
            Label(text_frame, text=f"🧂 {ing_text}", font=('Inter', 12),
                  bg="#1E1E1E", fg="#AAAAAA", wraplength=700,
                  justify=LEFT).pack(anchor="w", pady=(4, 0))