from datetime import datetime

class Airplane:
    """
    Класс, представляющий самолёт авиакомпании.

    Атрибуты:
        flight_number (str): Номер рейса
        available_seats (int): Количество свободных мест
        route (list): Маршрут следования [город вылета, город назначения]
        flight_date (datetime): Дата вылета
        seat_price (float): Стоимость места
    """

    def __init__(self, flight_number, available_seats, route, flight_date, seat_price):
        """
        Конструктор класса Airplane.

        Args:
            flight_number (str): Номер рейса
            available_seats (int): Количество свободных мест
            route (list): Маршрут [город вылета, город назначения]
            flight_date (datetime): Дата вылета
            seat_price (float): Стоимость места
        """
        self.flight_number = flight_number
        self.available_seats = available_seats
        self.route = route
        self.flight_date = flight_date
        self.seat_price = seat_price

    def has_route_and_date(self, departure_city, destination_city, flight_date):
        """
        Проверяет, есть ли рейс с заданным маршрутом и датой.

        Args:
            departure_city (str): Город вылета
            destination_city (str): Город назначения
            flight_date (datetime): Дата вылета

        Returns:
            bool: True, если маршрут и дата совпадают, иначе False
        """
        return (self.route[0] == departure_city and
                self.route[1] == destination_city and
                self.flight_date.date() == flight_date.date())

    def __str__(self):
        """Строковое представление самолёта."""
        return (f"Рейс: {self.flight_number}\n"
                f"Маршрут: {self.route[0]} → {self.route[1]}\n"
                f"Дата вылета: {self.flight_date.strftime('%d.%m.%Y')}\n"
                f"Свободных мест: {self.available_seats}\n"
                f"Стоимость места: {self.seat_price:.2f} руб.")