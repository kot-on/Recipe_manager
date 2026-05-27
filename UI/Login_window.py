from tkinter import *
from tkinter import ttk
import customtkinter

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
                                   )
entry_log.pack(pady=10) 
entry_pass = customtkinter.CTkEntry(root,
                                    placeholder_text="Пароль",
                                    width=212,
                                    height=49,
                                    corner_radius=10,
                                    font=('Inter',25)
                                    )
entry_pass.pack(pady=10) 
btn = customtkinter.CTkButton(root,
                              text="Войти",
                              width=212,
                              height=49,
                              fg_color='#63078E',
                              font=('Inter',30),
                              corner_radius=10
                              )
btn.pack(pady=10) 
btn2 = customtkinter.CTkButton(root,
                               text="Нет аккаунта",
                               width=104,
                               height=23,
                               fg_color='black',
                               font=('Inter',15, "underline"),
                               corner_radius=10,
                               text_color='#63078E',
                               )
btn2.pack(pady=10) 
root.mainloop()