"""Модели предметной области: пользователь, банковский счёт."""


class User:
    """Модель пользователя банка."""

    def __init__(self, username, password, first_name, last_name, balance=0):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.balance = balance

    def check_balance(self):
        return self.balance

    def transfer_money(self, recipient, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            return True
        return False

    def change_password(self, new_password):
        self.password = new_password

    def update_profile(self, new_first_name, new_last_name):
        self.first_name = new_first_name
        self.last_name = new_last_name


class BankAccount(User):
    """Счёт, привязанный к пользователю."""

    def __init__(self, account_number, owner, balance=0):
        super().__init__(
            owner.username, owner.password,
            owner.first_name, owner.last_name, balance,
        )
        self.account_number = account_number


class Profile(User):
    """Профиль (наследует User для гибкости расширения)."""

    def __init__(self, username, password, first_name, last_name):
        super().__init__(username, password, first_name, last_name)
