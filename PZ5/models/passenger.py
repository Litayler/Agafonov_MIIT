import random
from datetime import datetime

class Passenger:
    """
    Класс, представляющий пассажира авиакомпании.

    Атрибуты:
        first_name (str): Имя пассажира
        last_name (str): Фамилия пассажира
        patronymic (str): Отчество пассажира
        passport_number (str): Номер паспорта
        destination_airport (str): Аэропорт назначения
        account_balance (float): Состояние денежного счёта
        bonus_points (int): Количество бонусных баллов
        flight_date (datetime): Дата вылета
        flight_number (str): Номер рейса
        seat_number (str): Номер места в самолёте
    """

    def __init__(self, first_name, last_name, patronymic, passport_number,
                 destination_airport, account_balance, flight_date, flight_number=None, seat_number=None):
        """
        Конструктор класса Passenger.

        Args:
            first_name (str): Имя пассажира
            last_name (str): Фамилия пассажира
            patronymic (str): Отчество пассажира
            passport_number (str): Номер паспорта
            destination_airport (str): Аэропорт назначения
            account_balance (float): Начальный баланс счёта
            flight_date (datetime): Дата вылета
            flight_number (str, optional): Номер рейса. По умолчанию None.
            seat_number (str, optional): Номер места. По умолчанию None.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.passport_number = passport_number
        self.destination_airport = destination_airport
        self.account_balance = account_balance
        self.bonus_points = random.randint(0, 1000)  # Случайные бонусные баллы до 1000
        self.flight_date = flight_date
        self.flight_number = flight_number
        self.seat_number = seat_number

    def get_total_available_funds(self):
        """
        Возвращает предельное количество денежных средств пассажира с учётом счёта и бонусных баллов.

        Returns:
            float: Общая сумма доступных средств (счёт + бонусные баллы)
        """
        return self.account_balance + self.bonus_points

    def __str__(self):
        """Строковое представление пассажира."""
        return (f"Пассажир: {self.last_name} {self.first_name} {self.patronymic}\n"
                f"Паспорт: {self.passport_number}\n"
                f"Аэропорт назначения: {self.destination_airport}\n"
                f"Баланс: {self.account_balance:.2f} руб.\n"
                f"Бонусные баллы: {self.bonus_points}\n"
                f"Дата вылета: {self.flight_date.strftime('%d.%m.%Y')}")