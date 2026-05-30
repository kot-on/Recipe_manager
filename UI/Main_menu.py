from tkinter import *
def open_main_window():
    root = Tk()
    root.title("Login window")
    root.geometry("700x500")
    label = Label(text="Recipe manager",fg='#585B91',font=('Inter',50),bg='Black')
    label.pack()
    root.configure(bg='Black')
    root.mainloop()