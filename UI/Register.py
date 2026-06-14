from tkinter import *
from tkinter import messagebox
import customtkinter
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from AUTH.Register import register_user
from Main_menu import open_main_window
from PIL import Image,ImageTk
import re
from Logger_logic import AuditLogger

def open_register(root):
    reg_window = Toplevel()
    reg_window.title("Register window")
    reg_window.geometry("700x500")
    reg_window.configure(bg='Black')
    image_path = "Assets/Logo.png"
    pil_image = Image.open(image_path) 
    img = ImageTk.PhotoImage(pil_image)
    Image_label = Label(reg_window,image=img,bg='black')
    Image_label.image = img
    Image_label.pack(pady=(20,5))
    
    label = Label(reg_window, text="Регистрация", fg='#585B91', font=('Inter', 50), bg='Black')
    label.pack(pady=(0,20))

    entry_login = customtkinter.CTkEntry(reg_window,
                                         placeholder_text="Логин",
                                         width=212, height=49,
                                         corner_radius=10, font=('Inter', 25))
    entry_login.pack(pady=10)

    entry_pass = customtkinter.CTkEntry(reg_window,
                                        placeholder_text="Пароль",
                                        width=212, height=49,
                                        corner_radius=10, font=('Inter', 25),show='*')
    entry_pass.pack(pady=10)

    entry_pass2 = customtkinter.CTkEntry(reg_window,
                                         placeholder_text="Повторите пароль",
                                         width=212, height=49,
                                         corner_radius=10, font=('Inter', 25),show='*')
    entry_pass2.pack(pady=10)
    
    def register():
        username = entry_login.get()
        password1 = entry_pass.get()
        password2 = entry_pass2.get()

        if not re.match(r'^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~ ]+$', username):
            messagebox.showerror("Ошибка", "Логин должен содержать только латинские символы")
            return
    
        if not re.match(r'^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~ ]+$', password1):
            messagebox.showerror("Ошибка", "Пароль должен содержать только латинские символы")
            return

        if len(password1) < 8:
            messagebox.showerror("Ошибка", "Пароль должен содержать 8 и более символов")
            return

        if password1 == password2:
            User_id = register_user(username, password1)
            AuditLogger.log(User_id, username, "REGISTER", entity_type="USER", entity_id=User_id, details=f"Регистрация пользователя {username}", status="SUCCESS")
            reg_window.destroy()
            root.destroy()
            open_main_window(User_id, username)
        else:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
        return 

    btn_reg = customtkinter.CTkButton(reg_window,
                                      text="Зарегистрироваться",
                                      width=212, height=49,
                                      fg_color='#63078E', font=('Inter', 25),
                                      corner_radius=10,
                                      command=register)
    btn_reg.pack(pady=10)
