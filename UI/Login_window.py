import os
import sys
from tkinter import *
from tkinter import messagebox
import customtkinter
from Register import open_register # Нужно для перехода в регу
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # не видет другие файлы проекта, без этой команды
from AUTH.Login import login_user # нужно прописывать папку и файл + функция
from Main_menu import open_main_window #Переброс в главное меню
root = Tk()
root.title("Login window")
root.geometry("700x500")
label = Label(text="Recipe manager",fg='#585B91',font=('Inter',50),bg='Black')
label.pack()
root.configure(bg='Black')
entry_log = customtkinter.CTkEntry(root,
                                   placeholder_text="Логин",
                                   width=212,
                                   height=49,
                                   corner_radius=10,
                                   font=('Inter',25)
                                   ) #поля ввода логина
entry_log.pack(pady=10) 
entry_pass = customtkinter.CTkEntry(root,
                                    placeholder_text="Пароль",
                                    width=212,
                                    height=49,
                                    corner_radius=10,
                                    font=('Inter',25),show='*'
                                    ) #поля ввода пароля
entry_pass.pack(pady=10) 

def Gotoregister(): # функци для перехода в регу
    root.withdraw()
    open_register(root) 

def login(): # логин в приложение
    success = login_user(entry_log.get(), entry_pass.get())

    if success:
        root.destroy()  # закрываем окно логина
        
        open_main_window()  # пользователь вошел
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")
btn = customtkinter.CTkButton(root,
                              text="Войти",
                              width=212,
                              height=49,
                              fg_color='#63078E',
                              font=('Inter',30),
                              corner_radius=10,
                              command=login
                              ) #ВХОД
btn.pack(pady=10) 
btn2 = customtkinter.CTkButton(root,
                               text="Нет аккаунта",
                               width=104,
                               height=23,
                               fg_color='black',
                               font=('Inter',15, "underline"),
                               corner_radius=10,
                               text_color='#63078E',
                               command=Gotoregister) #Рега 
btn2.pack(pady=10) 
root.mainloop()