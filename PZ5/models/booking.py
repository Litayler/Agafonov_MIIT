class Booking:
    """
    Класс, представляющий бронирование билета.

    Атрибуты:
        flight_number (str): Номер рейса
        passport_number (str): Номер паспорта пассажира
        departure_airport (str): Аэропорт вылета
        destination_airport (str): Аэропорт назначения
        date (datetime): Дата вылета
        seat_price (float): Стоимость места
        seat_number (str): Номер места
    """

    def __init__(self):
        """Конструктор класса Booking."""
        self.flight_number = None
        self.passport_number = None
        self.departure_airport = None
        self.destination_airport = None
        self.date = None
        self.seat_price = None
        self.seat_number = None

    def make_booking(self, passenger, airplanes):
        """
        Осуществляет бронирование билета для пассажира.

        Args:
            passenger (Passenger): Объект пассажира
            airplanes (list): Список объектов самолётов

        Returns:
            bool: True, если бронирование успешно, иначе False
        """
        for airplane in airplanes:
            if (airplane.has_route_and_date(self.departure_airport, passenger.destination_airport, passenger.flight_date)
                    and airplane.available_seats > 0
                    and passenger.get_total_available_funds() >= airplane.seat_price):

                # Осуществляем бронирование
                self.flight_number = airplane.flight_number
                self.passport_number = passenger.passport_number
                self.destination_airport = passenger.destination_airport
                self.date = passenger.flight_date
                self.seat_price = airplane.seat_price
                self.seat_number = f"A{airplane.available_seats}"  # Простое присвоение номера места

                # Обновляем данные
                airplane.available_seats -= 1
                passenger.flight_number = airplane.flight_number
                passenger.seat_number = self.seat_number

                if passenger.account_balance >= airplane.seat_price:
                    passenger.account_balance -= airplane.seat_price
                else:
                    # Используем бонусные баллы
                    remaining = airplane.seat_price - passenger.account_balance
                    passenger.account_balance = 0
                    passenger.bonus_points -= remaining

                return True
        return False

    def print_booking_info(self):
        """Выводит в консоль информацию о забронированном билете."""
        if self.flight_number:
            print("\n=== ИНФОРМАЦИЯ О БРОНИРОВАНИИ ===")
            print(f"Номер рейса: {self.flight_number}")
            print(f"Аэропорт вылета: {self.departure_airport}")
            print(f"Аэропорт назначения: {self.destination_airport}")
            print(f"Дата вылета: {self.date.strftime('%d.%m.%Y')}")
            print(f"Стоимость места: {self.seat_price:.2f} руб.")
            print(f"Номер места: {self.seat_number}")
        else:
            print("\nБронирование не выполнено: подходящий рейс не найден или недостаточно средств.")