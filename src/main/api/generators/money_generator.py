import random
from faker import Faker

fake = Faker()

class MoneyGenerator:
    @staticmethod
    def valid_credit_amount() -> int:
        """Случайная сумма кредита по ТЗ (5000 - 15000)"""
        return fake.pyint(min_value=5000, max_value=15000)

    @staticmethod
    def valid_deposit_amount() -> float:
        """Случайная сумма депозита по ТЗ (1000.0 - 9000.0)"""
        return round(random.uniform(1000.0, 9000.0), 2)

    @staticmethod
    def max_deposit_amount() -> float:
        """Максимальная сумма депозита (9000.0)"""
        return 9000.0

    @staticmethod
    def valid_transfer_amount() -> float:
        """Случайная сумма перевода по ТЗ (500.0 - 10000.0)"""
        return round(random.uniform(500.0, 10000.0), 2)

    @staticmethod
    def credit_term_months() -> int:
        """Случайный срок кредита (6 - 36 месяцев)"""
        return fake.pyint(min_value=6, max_value=36)