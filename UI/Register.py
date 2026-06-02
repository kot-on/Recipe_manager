from tkinter import *
from tkinter import messagebox
import customtkinter
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) #тоже самое для видимости файлов
from AUTH.Register import register_user
from Main_menu import open_main_window #Переброс в главное меню
from PIL import Image,ImageTk
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
                                         corner_radius=10, font=('Inter', 25)) #Ввод логина
    entry_login.pack(pady=10)

    entry_pass = customtkinter.CTkEntry(reg_window,
                                        placeholder_text="Пароль",
                                        width=212, height=49,
                                        corner_radius=10, font=('Inter', 25),show='*') #Ввод пароля
    entry_pass.pack(pady=10)

    entry_pass2 = customtkinter.CTkEntry(reg_window,
                                         placeholder_text="Повторите пароль",
                                         width=212, height=49,
                                         corner_radius=10, font=('Inter', 25),show='*') # Ввод пароля для сверка
    entry_pass2.pack(pady=10)
    def register(): #Регистрация с проверкой пароля
        username = entry_login.get()
        password1 = entry_pass.get()
        password2 = entry_pass2.get()
        if password1 == password2:
            register_user(username,password1)
            root.destroy()
            open_main_window()
        else:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
        return 

    btn_reg = customtkinter.CTkButton(reg_window,
                                      text="Зарегистрироваться",
                                      width=212, height=49,
                                      fg_color='#63078E', font=('Inter', 25),
                                      corner_radius=10,
                                      command=register) #Кнопка реги
    btn_reg.pack(pady=10)
