import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tkinter import *
import customtkinter
from Database.db import show_3_recipes
from PIL import Image, ImageTk
def open_main_window(User_id):
    root = Tk()
    root.title("Login window")
    root.geometry("1200x800")
    root.configure(bg='Black')
    label = Label(root,text="Recipe manager",fg='#585B91',font=('Inter',50),bg='Black')
    label.pack()

    Add_button = customtkinter.CTkButton(root,width=600,height=100,corner_radius=15,font=('Inter',12),text='Добавить рецепт',fg_color="#F54927")
    Add_button.pack(pady=15)


    load_recipes(User_id,root)


    root.mainloop()


def load_recipes(User_id,root):
    recipe = show_3_recipes(User_id)

    if not recipe: 
        Label(
            root,
            text="У вас пока нет рецептов\nНажмите Добавить чтобы создать свой первый рецепт!",
            font=('Inter', 16),
            fg="gray"
        ).grid( row=1, column=0, expand=True) 
        return

    for i, row in enumerate(recipe):
        title = row[0]
        description = row[1]
        rating=row[2]
        image_path = row[3]
        recipe_card = Frame(root,bg="#D15555" )
        recipe_card.grid( row=i, column=0, padx=10, pady=10)
        
        try:
            img = Image.open(image_path)
            img = img.resize((150,150))
            photo = ImageTk.PhotoImage(img)
        except:
            photo = ImageTk.PhotoImage(file="Default.png")
        img_label = Label(recipe_card, image=photo)
        img_label.image = photo
        img_label.grid(row=i, column=0, padx=10, pady=10)

        Label(recipe_card, text=title, font=('Inter', 16),bg='Black',fg='white').grid(row=i, column=0, padx=10, pady=10)
        Label(recipe_card, text=f"Рейтинг: {rating}",bg='Black',fg='white').grid(row=i, column=2, padx=10, pady=10)
        Label(recipe_card, text=description,bg='Black',fg='white').grid(row=i, column=0, padx=10, pady=10)
if __name__ == "__main__":
    open_main_window(User_id=1)