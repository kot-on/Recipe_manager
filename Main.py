import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'UI'))
sys.path.insert(0, os.path.dirname(__file__))

from Database.DB_backup import check_integrity
from UI.Login_window import run_app

if __name__ == "__main__":
    if not check_integrity():
        from tkinter import messagebox
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Предупреждение", "ВНИМАНИЕ! База данных была изменена извне!")
        root.destroy()
    run_app()