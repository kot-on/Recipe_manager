import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tkinter import *
from tkinter import filedialog, messagebox
import customtkinter
from PIL import Image, ImageTk
import shutil
import uuid
from Database.db import save_recipe as db_save_recipes
from Logger_logic import AuditLogger
from Database.DB_backup import backup_before_change

def open_recipe_manager(root_parent, User_id, username=None, on_save=None):
    root = Toplevel(root_parent)
    root.title("Новый рецепт")
    root.geometry("1600x1000")
    root.configure(bg='Black')

    pil_image = Image.open("Assets/Logo.png")
    img_logo = ImageTk.PhotoImage(pil_image)
    logo_label = Label(root, image=img_logo, bg='Black')
    logo_label.image = img_logo
    logo_label.pack(pady=(20, 5))

    Label(root, text="Новый рецепт", fg='#585B91',font=('Inter', 30), bg='Black').pack(pady=(0, 10))

    image_frame = Frame(root, bg='#1E1E1E', width=300, height=200)
    image_frame.pack(pady=10)
    image_frame.pack_propagate(False)

    preview_label = Label(image_frame, text="Нажмите чтобы\nдобавить фото",
                          bg='#1E1E1E', fg='gray', font=('Inter', 14), cursor="hand2")
    preview_label.pack(expand=True)

    selected_image_path = StringVar(value="")

    def choose_image(event=None):
        path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png *.jpg *.jpeg *.webp")])
        if path:
            selected_image_path.set(path)
            img = Image.open(path).resize((300, 200))
            photo = ImageTk.PhotoImage(img)
            preview_label.configure(image=photo, text="")
            preview_label.image = photo

    preview_label.bind("<Button-1>", choose_image)

    center_frame = Frame(root, bg='Black')
    center_frame.pack(anchor="center")

    Label(center_frame, text="Название рецепта", fg='white',
      font=('Inter', 16), bg='Black').pack(anchor="w", pady=(15, 0))

    entry_title = customtkinter.CTkEntry(center_frame, placeholder_text="Например: Борщ",
                                     width=620, height=45,
                                     corner_radius=10, font=('Inter', 18))
    entry_title.pack()
    Label(center_frame, text="Описание", fg='white',
      font=('Inter', 16), bg='Black').pack(anchor="w", pady=(15, 0))

    entry_description = customtkinter.CTkTextbox(center_frame, width=620, height=100,
                                              corner_radius=10, font=('Inter', 16))
    entry_description.pack()
    Label(center_frame, text="Ингредиенты", fg='white',
      font=('Inter', 16), bg='Black').pack(anchor="w", pady=(15, 5))

    ingredients_frame = Frame(center_frame, bg='Black')
    ingredients_frame.pack()
    ingredient_rows = []

    def add_ingredient_row():
        row_frame = Frame(ingredients_frame, bg='Black')
        row_frame.pack(fill=X, pady=4)

        name_entry = customtkinter.CTkEntry(row_frame, placeholder_text="Название",width=280, height=40,corner_radius=10, font=('Inter', 16))
        name_entry.pack(side=LEFT, padx=(0, 10))

        amount_entry = customtkinter.CTkEntry(row_frame, placeholder_text="Кол-во",width=100, height=40,corner_radius=10, font=('Inter', 16))
        amount_entry.pack(side=LEFT, padx=(0, 10))

        unit_var = StringVar(value="г")
        unit_menu = customtkinter.CTkOptionMenu(row_frame, values=["г", "мл", "шт", "ст.л", "ч.л"],variable=unit_var,width=100, height=40,font=('Inter', 16))
        unit_menu.pack(side=LEFT, padx=(0, 10))

        delete_btn = customtkinter.CTkButton(row_frame, text="X", width=40, height=40,fg_color="#F54927", corner_radius=10,font=('Inter', 16),command=lambda: remove_row(row_frame, entry))
        delete_btn.pack(side=LEFT)

        entry = (name_entry, amount_entry, unit_var)
        ingredient_rows.append(entry)
        return entry

    def remove_row(frame, entry):
        frame.destroy()
        if entry in ingredient_rows:
            ingredient_rows.remove(entry)

    add_ingredient_row()

    customtkinter.CTkButton(center_frame, text="+ Добавить ингредиент",width=300, height=40, corner_radius=10,font=('Inter', 16), fg_color="#63078E",command=add_ingredient_row).pack(pady=10)

    Label(center_frame, text="Рейтинг", fg='white',
      font=('Inter', 16), bg='Black').pack(anchor="w", pady=(15, 0))

    rating_var = IntVar(value=0)
    stars_frame = Frame(center_frame, bg='Black')
    stars_frame.pack(anchor="w")

    star_buttons = []

    def set_rating(value):
        rating_var.set(value)
        for i, btn in enumerate(star_buttons):
            if i < value:
                btn.configure(text="★", text_color="#FFD700")
            else:
                btn.configure(text="☆", text_color="gray")

    for i in range(1, 6):
        btn = customtkinter.CTkButton(stars_frame, text="☆", width=45, height=45,
                                   fg_color="black", font=('Inter', 28),
                                   text_color="gray", corner_radius=5,
                                   hover_color="#1E1E1E",
                                   command=lambda v=i: set_rating(v))
        btn.pack(side=LEFT, padx=2)
        star_buttons.append(btn)
    
    def save_recipe():
        # Создаём бэкап перед изменением БД
        backup_before_change("create_recipe")
        
        title = entry_title.get().strip()
        description = entry_description.get("1.0", "end").strip()
        rating = rating_var.get()
        src_path = selected_image_path.get()

        if not title:
            messagebox.showerror("Ошибка", "Введите название рецепта")
            return

        ingredients = []
        for name_e, amount_e, unit_v in ingredient_rows:
            name = name_e.get().strip()
            amount = amount_e.get().strip()
            unit = unit_v.get()
            if name and amount:
                ingredients.append((name, amount, unit))

        if not ingredients:
            messagebox.showerror("Ошибка", "Добавьте хотя бы один ингредиент")
            return

        if src_path:
            ext = os.path.splitext(src_path)[1]
            unique_name = f"{uuid.uuid4().hex}{ext}"
            dest_path = os.path.join("Assets", "recipes", unique_name)
            shutil.copy(src_path, dest_path)
        else:
            dest_path = os.path.join("Assets", "default.png")

        try:
            recipe_id = db_save_recipes(User_id, title, description, rating, dest_path, ingredients)
            current_username = username if username else f"user_{User_id}"
            AuditLogger.log(User_id, current_username, "CREATE_RECIPE", entity_type="RECIPE", entity_id=recipe_id, details=f"Создан рецепт: {title}", status="SUCCESS")
            messagebox.showinfo("Готово", f"Рецепт «{title}» сохранён!")
            root.destroy()
            if on_save:
                on_save()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    customtkinter.CTkButton(center_frame, text="Сохранить рецепт",width=620, height=55, corner_radius=15,font=('Inter', 22), fg_color="#F54927",command=save_recipe).pack(pady=15)

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    open_recipe_manager(root, User_id=1)
    root.mainloop()
