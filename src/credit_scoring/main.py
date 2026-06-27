"""CLI-точка входа для расчёта кредитного потенциала."""

from src.credit_scoring.calculator import CreditCalculator
from src.credit_scoring.strategies import (
    IncomeAndLoanBasedStrategy,
    CreditHistoryBasedStrategy,
)


def choose_strategy():
    """Интерактивный выбор стратегии расчёта."""
    print("Выберите стратегию расчета кредитного потенциала:")
    print("1. На основе дохода")
    print("2. На основе кредитной истории")
    choice = input("Введите номер стратегии: ")

    if choice == "1":
        return IncomeAndLoanBasedStrategy()
    elif choice == "2":
        return CreditHistoryBasedStrategy()
    else:
        print("Неверный выбор.")
        return choose_strategy()


def main():
    strategy = choose_strategy()
    calculator = CreditCalculator(strategy)
    user_data = strategy.get_input()
    credit_potential = calculator.calculate_credit_potential(user_data)
    print("Кредитный потенциал:", credit_potential)


if __name__ == "__main__":
    main()
