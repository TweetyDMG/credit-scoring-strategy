"""Стратегии расчёта кредитного потенциала (паттерн Strategy)."""


class BaseStrategy:
    """Базовый интерфейс стратегии скоринга."""

    def calculate(self, user_data: dict) -> str:
        """Рассчитать кредитный потенциал на основе данных пользователя."""
        raise NotImplementedError("Subclasses should implement this method.")

    def get_input(self) -> dict:
        """Запросить у пользователя входные данные для стратегии."""
        pass


class IncomeAndLoanBasedStrategy(BaseStrategy):
    """Стратегия на основе ежемесячного дохода и желаемой суммы кредита."""

    def get_input(self) -> dict:
        income = float(input("Введите ваш ежемесячный доход: "))
        loan_amount = float(input("Введите желаемую сумму кредита: "))
        return {"income": income, "loan_amount": loan_amount}

    def calculate(self, user_data: dict) -> str:
        income = user_data.get("income", 0)
        loan_amount = user_data.get("loan_amount", 0)

        if income >= 60000 and loan_amount <= 50000:
            return "Высокий"
        elif income >= 40000 and loan_amount <= 30000:
            return "Средний"
        else:
            return "Низкий"


class CreditHistoryBasedStrategy(BaseStrategy):
    """Стратегия на основе кредитного рейтинга."""

    def get_input(self) -> dict:
        credit_score = int(input("Введите ваш кредитный рейтинг: "))
        return {"credit_score": credit_score}

    def calculate(self, user_data: dict) -> str:
        credit_score = user_data.get("credit_score", 0)

        if credit_score >= 700:
            return "Высокий"
        elif 600 <= credit_score < 700:
            return "Средний"
        else:
            return "Низкий"
