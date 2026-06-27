"""GUI-клиент банковского приложения на tkinter."""

import tkinter as tk
from tkinter import messagebox

from src.bank_app.models import User


class BankAppGUI:
    """Главное окно банковского приложения."""

    def __init__(self, root):
        self.root = root
        self.root.title("Bank App")

        self.current_user = None

        # Размещение окна по центру экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 500
        window_height = 500
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Демо-данные
        self.users = [
            User("1", "1", "John", "Doe", 1000),
            User("user2", "password2", "Jane", "Smith", 2000),
        ]

        self._build_login_screen()
        self.root.update_idletasks()

    # ─── Форма входа ────────────────────────────────────

    def _build_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=5)

        tk.Label(self.login_frame, text="Логин:").grid(row=0, column=0, padx=5, pady=5)
        self.login_entry = tk.Entry(self.login_frame)
        self.login_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Пароль:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(
            self.login_frame, text="Войти", command=self.login,
        )
        self.login_button.grid(row=2, columnspan=2, padx=5, pady=5)

    # ─── Авторизация ────────────────────────────────────

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        if self._check_credentials(username, password):
            self.current_user = self._get_user(username)
            self._show_dashboard()
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль")

    def _check_credentials(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def _get_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    # ─── Дашборд ────────────────────────────────────────

    def _show_dashboard(self):
        self.login_frame.destroy()
        if hasattr(self, "dashboard_frame"):
            self.dashboard_frame.destroy()

        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack(padx=10, pady=5)

        # Приветствие
        welcome_text = f"Добро пожаловать, {self.current_user.first_name}!"
        self.welcome_label = tk.Label(self.dashboard_frame, text=welcome_text)
        self.welcome_label.grid(row=0, columnspan=2, padx=5, pady=5)

        # Баланс
        self.balance_label = tk.Label(
            self.dashboard_frame,
            text=f"Ваш баланс: {self.current_user.check_balance()} руб.",
        )
        self.balance_label.grid(row=1, columnspan=2, padx=5, pady=5)

        self._build_transfer_form()
        self._build_profile_form()
        self._build_deposit_form()

        tk.Label(
            self.dashboard_frame,
            text="Вы вошли в демо счет",
            font=("Helvetica", 9),
            fg="red",
        ).grid(row=7, columnspan=2, sticky="se", padx=5, pady=5)

        tk.Button(
            self.dashboard_frame, text="Выйти", command=self.logout,
        ).grid(row=6, columnspan=2, padx=5, pady=5)

        self.root.update_idletasks()

    # ─── Переводы ───────────────────────────────────────

    def _build_transfer_form(self):
        frame = tk.Frame(self.dashboard_frame)
        frame.grid(row=2, column=0, padx=5, pady=5)

        tk.Label(frame, text="Совершить перевод", font=("Helvetica", 11, "bold"))\
            .grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(frame, text="Получатель:").grid(row=1, column=0, padx=5, pady=5)
        recipient_entry = tk.Entry(frame)
        recipient_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Сумма:").grid(row=2, column=0, padx=5, pady=5)
        amount_entry = tk.Entry(frame)
        amount_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(
            frame,
            text="Перевести",
            command=lambda: self._transfer_money(
                recipient_entry.get(), amount_entry.get(),
            ),
        ).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def _transfer_money(self, recipient_username, amount_str):
        if not recipient_username or not amount_str:
            messagebox.showerror("Ошибка", "Введите получателя и сумму для перевода")
            return

        recipient = self._get_user(recipient_username)
        if recipient is None:
            messagebox.showerror("Ошибка", "Пользователь с таким именем не найден")
            return

        if recipient == self.current_user:
            messagebox.showerror("Ошибка", "Вы не можете перевести деньги самому себе")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму для перевода")
            return

        if self.current_user.transfer_money(recipient, amount):
            messagebox.showinfo("Успех", f"Перевод успешно выполнен: {amount} руб.")
            self._update_balance_label()
        else:
            messagebox.showerror("Ошибка", "Недостаточно средств для перевода")

    # ─── Профиль ────────────────────────────────────────

    def _build_profile_form(self):
        frame = tk.Frame(self.dashboard_frame)
        frame.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Изменить профиль", font=("Helvetica", 11, "bold"))\
            .grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(frame, text="Имя:").grid(row=2, column=0, padx=5, pady=5)
        first_name_entry = tk.Entry(frame)
        first_name_entry.insert(0, self.current_user.first_name)
        first_name_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Фамилия:").grid(row=3, column=0, padx=5, pady=5)
        last_name_entry = tk.Entry(frame)
        last_name_entry.insert(0, self.current_user.last_name)
        last_name_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Пароль:").grid(row=4, column=0, padx=5, pady=5)
        password_entry = tk.Entry(frame, show="*")
        password_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(
            frame,
            text="Изменить",
            command=lambda: self._change_profile(
                first_name_entry.get(),
                last_name_entry.get(),
                password_entry.get(),
                first_name_entry, last_name_entry, password_entry,
            ),
        ).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def _change_profile(self, new_first_name, new_last_name, new_password,
                        first_name_entry, last_name_entry, password_entry):
        if not new_first_name or not new_last_name or not new_password:
            messagebox.showerror("Ошибка", "Введите имя, фамилию и пароль")
            return

        self.current_user.first_name = new_first_name
        self.welcome_label.config(
            text=f"Добро пожаловать, {self.current_user.first_name}!",
        )
        self.current_user.update_profile(new_first_name, new_last_name)
        self.current_user.change_password(new_password)

        messagebox.showinfo("Успех", "Данные профиля успешно изменены")
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    # ─── Пополнение счёта ───────────────────────────────

    def _build_deposit_form(self):
        frame = tk.Frame(self.dashboard_frame)
        frame.grid(row=3, column=0, padx=5, pady=5)

        tk.Label(frame, text="Положить деньги на счет", font=("Helvetica", 11, "bold"))\
            .grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(frame, text="Сумма:").grid(row=1, column=0, padx=5, pady=5)
        amount_entry = tk.Entry(frame)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            frame,
            text="Пополнить счет",
            command=lambda: self._deposit_money(amount_entry.get()),
        ).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def _deposit_money(self, amount_str):
        if not amount_str:
            messagebox.showerror("Ошибка", "Введите сумму для пополнения счета")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму для пополнения счета")
            return

        if amount <= 0:
            messagebox.showerror("Ошибка", "Введите положительную сумму для пополнения счета")
            return

        self.current_user.balance += amount
        messagebox.showinfo("Успех", f"Счет успешно пополнен на {amount} руб.")
        self._update_balance_label()

    # ─── Вспомогательное ────────────────────────────────

    def _update_balance_label(self):
        if hasattr(self, "balance_label") and self.current_user:
            self.balance_label.config(
                text=f"Ваш баланс: {self.current_user.check_balance()} руб.",
            )

    def logout(self):
        self.root.destroy()
