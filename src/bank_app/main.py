"""GUI-точка входа банковского приложения."""

import tkinter as tk
from src.bank_app.gui import BankAppGUI


def main():
    root = tk.Tk()
    BankAppGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
