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
    Add_button.pack()

    left_frame = Frame(root)
    left_frame.pack(side=LEFT,fill=BOTH,expand=True)
    right_frame = Frame(root)
    right_frame.pack(side=LEFT,fill=BOTH,expand=True)
    load_recipes(left_frame,right_frame,User_id)


    root.mainloop()


def load_recipes(left_frame,right_frame,User_id):
    recipe = show_3_recipes(User_id)

    if not recipe:  # список пустой
        Label(
            right_frame,
            text="У вас пока нет рецептов\nНажмите Добавить чтобы создать свой первый рецепт!",
            font=('Inter', 16),
            fg="gray"
        ).pack(expand=True) 
        return

    for i, row in enumerate(recipe):
        title = recipe[0]
        description = recipe[1]
        rating=recipe[2]
        image_path = recipe[3]

        try:
            img = Image.open(image_path)
            img = img.resize((150,150))
            photo = ImageTk.PhotoImage(img)
        except:
            photo = ImageTk.PhotoImage(file="Default.png")
        img_label = Label(left_frame, image=photo)
        img_label.image = photo
        img_label.grid(row=i, column=0, padx=10, pady=10)

        Label(right_frame, text=title, font=('Inter', 16)).grid(row=i, column=0)
        Label(right_frame, text=f"Рейтинг: {rating}").grid(row=i, column=1)
        Label(right_frame, text=description).grid(row=i, column=2)
if __name__ == "__main__":
    open_main_window(User_id=1)