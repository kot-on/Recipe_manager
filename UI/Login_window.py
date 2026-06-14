import os
import sys
from tkinter import *
from tkinter import messagebox
import customtkinter
from Register import open_register
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from AUTH.Login import login_user
from Main_menu import open_main_window
from PIL import Image,ImageTk
import re

root = Tk()
root.title("Login window")
root.geometry("700x500")
image_path = "Assets/Logo.png"
pil_image = Image.open(image_path)
img = ImageTk.PhotoImage(pil_image)
Image_label = Label(root,image=img,bg='black')
Image_label.pack(pady=(20,5))
label = Label(text="Recipe manager",fg='#585B91',font=('Inter',50),bg='Black')
label.pack(pady=(0,20))
root.configure(bg='Black')
entry_log = customtkinter.CTkEntry(root,
                                   placeholder_text="Логин",
                                   width=212,
                                   height=49,
                                   corner_radius=10,
                                   font=('Inter',25))
entry_log.pack(pady=10) 
entry_pass = customtkinter.CTkEntry(root,
                                    placeholder_text="Пароль",
                                    width=212,
                                    height=49,
                                    corner_radius=10,
                                    font=('Inter',25),show='*')
entry_pass.pack(pady=10) 

def Gotoregister():
    root.withdraw()
    open_register(root) 

def login():
    username = entry_log.get()
    password = entry_pass.get()

    if not re.match(r'^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~ ]+$', username):
        messagebox.showerror("Ошибка", "Логин должен содержать только латинские символы")
        return
    
    if not re.match(r'^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~ ]+$', password):
        messagebox.showerror("Ошибка", "Пароль должен содержать только латинские символы")
        return

    User_id = login_user(username, password)

    if User_id:
        root.destroy()
        open_main_window(User_id, username)  # ← ИСПРАВЛЕНО
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

btn = customtkinter.CTkButton(root,
                              text="Войти",
                              width=212,
                              height=49,
                              fg_color='#63078E',
                              font=('Inter',30),
                              corner_radius=10,
                              command=login)
btn.pack(pady=10) 
btn2 = customtkinter.CTkButton(root,
                               text="Нет аккаунта",
                               width=104,
                               height=23,
                               fg_color='black',
                               font=('Inter',15, "underline"),
                               corner_radius=10,
                               text_color='#63078E',
                               command=Gotoregister)
btn2.pack(pady=10) 
root.mainloop()
