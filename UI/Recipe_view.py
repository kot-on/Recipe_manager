import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tkinter import *
from tkinter import messagebox, filedialog
import customtkinter
from Database.db import get_all_recipes, delete_recipe, update_recipe
from PIL import Image, ImageTk
from UI_logger import log_ui_action
import shutil
import uuid

def open_all_recipes(root_parent, User_id, username,on_main_refresh=None):
    log_ui_action(username, "Открыть все рецепты")
    root = Toplevel(root_parent)
    root.title("Все рецепты")
    root.geometry("1200x800")
    root.configure(bg='Black')
    def refresh():
        for widget in inner_frame.winfo_children():
            widget.destroy()
        load_all_recipes(User_id, username, inner_frame, refresh)
        if on_main_refresh:
            on_main_refresh()
    pil_image = Image.open("Assets/Logo.png")
    img_logo = ImageTk.PhotoImage(pil_image)
    logo_label = Label(root, image=img_logo, bg='Black')
    logo_label.image = img_logo
    logo_label.pack(pady=(20, 5))

    Label(root, text="Мои рецепты", fg='#585B91',
          font=('Inter', 40), bg='Black').pack(pady=(0, 10))
    def go_back():
        log_ui_action(username, "Назад — вернуться в главное меню")
        if on_main_refresh:
            on_main_refresh()
        root_parent.deiconify()
        root.destroy()

    customtkinter.CTkButton(
        root, text="← Назад", width=150, height=35,
        fg_color="#1E1E1E", font=('Inter', 14), corner_radius=8,
        text_color="white", hover_color="#333333",
        command=go_back
    ).pack(pady=(0, 10))

    
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

    def refresh():
        for widget in inner_frame.winfo_children():
            widget.destroy()
        load_all_recipes(User_id, username, inner_frame, refresh)

    load_all_recipes(User_id, username, inner_frame, refresh)


def load_all_recipes(User_id, username, frame, refresh):
    recipes = get_all_recipes(User_id)

    if not recipes:
        Label(frame,
              text="У вас пока нет рецептов\nНажмите «Добавить» чтобы создать первый!",
              font=('Inter', 16), fg="gray", bg="Black").pack(expand=True, pady=50)
        return

    for recipe in recipes:
        card = Frame(frame, bg="#1E1E1E", pady=10)
        card.pack(fill=X, padx=20, pady=10)

        try:
            img = Image.open(recipe["image_path"]).resize((150, 150))
            photo = ImageTk.PhotoImage(img)
        except:
            img = Image.open("Assets/default.png").resize((150, 150))
            photo = ImageTk.PhotoImage(img)

        img_label = Label(card, image=photo, bg="#1E1E1E")
        img_label.image = photo
        img_label.pack(side=LEFT, padx=15)

        text_frame = Frame(card, bg="#1E1E1E")
        text_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        Label(text_frame, text=recipe["title"], font=('Inter', 20, 'bold'),
              bg="#1E1E1E", fg="white", anchor="w").pack(anchor="w")

        Label(text_frame, text=f"⭐ Рейтинг: {recipe['rating']}",
              font=('Inter', 14), bg="#1E1E1E", fg="#FFD700").pack(anchor="w", pady=4)

        Label(text_frame, text=recipe["description"], font=('Inter', 13),
              bg="#1E1E1E", fg="#CCCCCC", wraplength=700, justify=LEFT).pack(anchor="w")

        if recipe["ingredients"]:
            ing_text = "  •  ".join([f"{name} {amount}{unit}"
                                     for name, amount, unit in recipe["ingredients"]])
            Label(text_frame, text=f"🧂 {ing_text}", font=('Inter', 12),
                  bg="#1E1E1E", fg="#AAAAAA", wraplength=700,
                  justify=LEFT).pack(anchor="w", pady=(4, 0))

        btn_frame = Frame(card, bg="#1E1E1E")
        btn_frame.pack(side=RIGHT, padx=15)

        customtkinter.CTkButton(
            btn_frame, text="Изменить", width=100, height=35,
            fg_color="#63078E", font=('Inter', 14), corner_radius=8,
            command=lambda r=recipe: [
                log_ui_action(username, f"Изменить рецепт: {r['title']}"),
                open_edit_window(r, username, refresh)
            ]
        ).pack(pady=(0, 8))

        customtkinter.CTkButton(
            btn_frame, text="Удалить", width=100, height=35,
            fg_color="#F54927", font=('Inter', 14), corner_radius=8,
            command=lambda r=recipe: confirm_delete(r, username, refresh)
        ).pack()


def confirm_delete(recipe, username, refresh):
    log_ui_action(username, f"Удалить рецепт: {recipe['title']}")
    if messagebox.askyesno("Подтверждение", f"Удалить рецепт «{recipe['title']}»?"):
        delete_recipe(recipe["id"])
        refresh()


def open_edit_window(recipe, username, refresh):
    win = Toplevel()
    win.title("Редактировать рецепт")
    win.geometry("700x900")
    win.configure(bg='Black')

    canvas = Canvas(win, bg='Black', highlightthickness=0)
    scrollbar = Scrollbar(win, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    center = Frame(canvas, bg='Black')
    canvas_window = canvas.create_window((0, 0), window=center, anchor="n")

    def on_canvas_resize(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", on_canvas_resize)

    def on_frame_resize(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    center.bind("<Configure>", on_frame_resize)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    Label(center, text="Редактировать рецепт", fg='#585B91',
          font=('Inter', 28), bg='Black').pack(pady=(20, 10))

    # Фото
    selected_image_path = StringVar(value=recipe["image_path"])

    try:
        img = Image.open(recipe["image_path"]).resize((200, 140))
        photo = ImageTk.PhotoImage(img)
    except:
        img = Image.open("Assets/default.png").resize((200, 140))
        photo = ImageTk.PhotoImage(img)

    preview = Label(center, image=photo, bg='Black', cursor="hand2")
    preview.image = photo
    preview.pack(pady=(0, 5))
    Label(center, text="Нажмите на фото чтобы изменить",
          fg='gray', font=('Inter', 11), bg='Black').pack()

    def choose_image(event=None):
        path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png *.jpg *.jpeg *.webp")])
        if path:
            log_ui_action(username, "Изменить фото рецепта")
            selected_image_path.set(path)
            img2 = Image.open(path).resize((200, 140))
            photo2 = ImageTk.PhotoImage(img2)
            preview.configure(image=photo2)
            preview.image = photo2

    preview.bind("<Button-1>", choose_image)

    # Название
    Label(center, text="Название", fg='white', font=('Inter', 14), bg='Black').pack(anchor="w", padx=50, pady=(10, 0))
    entry_title = customtkinter.CTkEntry(center, width=500, height=40, font=('Inter', 16))
    entry_title.insert(0, recipe["title"])
    entry_title.pack()

    # Описание
    Label(center, text="Описание", fg='white', font=('Inter', 14), bg='Black').pack(anchor="w", padx=50, pady=(10, 0))
    entry_desc = customtkinter.CTkTextbox(center, width=500, height=80, font=('Inter', 14))
    entry_desc.insert("1.0", recipe["description"])
    entry_desc.pack()

    # Ингредиенты
    Label(center, text="Ингредиенты", fg='white', font=('Inter', 14), bg='Black').pack(anchor="w", padx=50, pady=(10, 5))

    ingredients_frame = Frame(center, bg='Black')
    ingredients_frame.pack()
    ingredient_rows = []

    def add_ingredient_row(name="", amount="", unit="г"):
        row_frame = Frame(ingredients_frame, bg='Black')
        row_frame.pack(fill=X, pady=4)

        name_entry = customtkinter.CTkEntry(row_frame, placeholder_text="Название",
                                            width=220, height=38, corner_radius=10, font=('Inter', 14))
        name_entry.pack(side=LEFT, padx=(0, 6))
        if name:
            name_entry.insert(0, name)

        amount_entry = customtkinter.CTkEntry(row_frame, placeholder_text="Кол-во",
                                              width=90, height=38, corner_radius=10, font=('Inter', 14))
        amount_entry.pack(side=LEFT, padx=(0, 6))
        if amount:
            amount_entry.insert(0, amount)

        unit_var = StringVar(value=unit)
        unit_menu = customtkinter.CTkOptionMenu(row_frame, values=["г", "мл", "шт", "ст.л", "ч.л"],
                                                variable=unit_var, width=90, height=38, font=('Inter', 14))
        unit_menu.pack(side=LEFT, padx=(0, 6))

        entry = (name_entry, amount_entry, unit_var)

        delete_btn = customtkinter.CTkButton(
            row_frame, text="X", width=38, height=38,
            fg_color="#F54927", corner_radius=10, font=('Inter', 14),
            command=lambda: [
                log_ui_action(username, "Удалить ингредиент"),
                remove_row(row_frame, entry)
            ]
        )
        delete_btn.pack(side=LEFT)
        ingredient_rows.append(entry)
        return entry

    def remove_row(frame, entry):
        frame.destroy()
        if entry in ingredient_rows:
            ingredient_rows.remove(entry)

    for name, amount, unit in recipe["ingredients"]:
        add_ingredient_row(name, amount, unit)

    if not recipe["ingredients"]:
        add_ingredient_row()

    customtkinter.CTkButton(
        center, text="+ Добавить ингредиент", width=300, height=38,
        corner_radius=10, font=('Inter', 14), fg_color="#63078E",
        command=lambda: [
            log_ui_action(username, "Добавить ингредиент"),
            add_ingredient_row()
        ]
    ).pack(pady=8)

    # Рейтинг
    Label(center, text="Рейтинг", fg='white', font=('Inter', 14), bg='Black').pack(anchor="w", padx=50, pady=(10, 0))
    rating_var = IntVar(value=recipe["rating"])
    stars_frame = Frame(center, bg='Black')
    stars_frame.pack()
    star_buttons = []

    def set_rating(value):
        log_ui_action(username, f"Выбрать рейтинг: {value} звёзд")
        rating_var.set(value)
        for i, btn in enumerate(star_buttons):
            btn.configure(text="★" if i < value else "☆",
                          text_color="#FFD700" if i < value else "gray")

    for i in range(1, 6):
        btn = customtkinter.CTkButton(
            stars_frame, text="★" if i <= recipe["rating"] else "☆",
            width=40, height=40, fg_color="black", font=('Inter', 24),
            text_color="#FFD700" if i <= recipe["rating"] else "gray",
            corner_radius=5, hover_color="#1E1E1E",
            command=lambda v=i: set_rating(v)
        )
        btn.pack(side=LEFT, padx=2)
        star_buttons.append(btn)

    # Сохранить
    def save_changes():
        title = entry_title.get().strip()
        description = entry_desc.get("1.0", "end").strip()
        rating = rating_var.get()
        src_path = selected_image_path.get()

        if not title:
            log_ui_action(username, "Сохранить изменения — ошибка: нет названия")
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
            log_ui_action(username, "Сохранить изменения — ошибка: нет ингредиентов")
            messagebox.showerror("Ошибка", "Добавьте хотя бы один ингредиент")
            return

        if src_path != recipe["image_path"]:
            ext = os.path.splitext(src_path)[1]
            unique_name = f"{uuid.uuid4().hex}{ext}"
            dest_path = os.path.join("Assets", "recipes", unique_name)
            shutil.copy(src_path, dest_path)
        else:
            dest_path = src_path

        update_recipe(recipe["id"], title, description, rating, dest_path, ingredients)
        log_ui_action(username, f"Сохранить изменения рецепта: {title}")
        messagebox.showinfo("Готово", f"Рецепт «{title}» обновлён!")
        win.destroy()
        refresh()

    customtkinter.CTkButton(
        center, text="Сохранить изменения", width=500, height=50,
        fg_color="#F54927", font=('Inter', 18), corner_radius=10,
        command=save_changes
    ).pack(pady=20)