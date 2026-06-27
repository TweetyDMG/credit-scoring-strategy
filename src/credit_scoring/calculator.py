"""Контекст для стратегий расчёта кредитного потенциала."""

from src.credit_scoring.strategies import BaseStrategy


class CreditCalculator:
    """Калькулятор, использующий переданную стратегию для расчёта."""

    def __init__(self, strategy: BaseStrategy):
        self.strategy = strategy

    def calculate_credit_potential(self, user_data: dict) -> str:
        """Делегирует расчёт выбранной стратегии."""
        return self.strategy.calculate(user_data)
