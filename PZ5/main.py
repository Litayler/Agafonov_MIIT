from datetime import datetime
from models.passenger import Passenger
from models.airplane import Airplane
from models.booking import Booking

def create_sample_airplanes():
    """Создаёт массив тестовых самолётов."""
    airplanes = [
        Airplane(
            flight_number="SU101",
            available_seats=150,
            route=["Москва", "Санкт-Петербург"],
            flight_date=datetime(2024, 12, 25),
            seat_price=5000.0
        ),
        Airplane(
            flight_number="SU202",
            available_seats=80,
            route=["Москва", "Сочи"],
            flight_date=datetime(2024, 12, 25),
            seat_price=8000.0
        ),
        Airplane(
            flight_number="SU303",
            available_seats=50,
            route=["Санкт-Петербург", "Казань"],
            flight_date=datetime(2024, 12, 26),
            seat_price=6000.0
        ),
        Airplane(
            flight_number="SU404",
            available_seats=200,
            route=["Москва", "Екатеринбург"],
            flight_date=datetime(2024, 12, 27),
            seat_price=7000.0
        ),
        Airplane(
            flight_number="SU505",
            available_seats=0,  # Нет свободных мест для тестирования
            route=["Москва", "Новосибирск"],
            flight_date=datetime(2024, 12, 28),
            seat_price=10000.0
        )
    ]
    return airplanes

def input_passenger_data():
    """Вводит данные пассажира с консоли."""
    print("=== ВВОД ДАННЫХ ПАССАЖИРА ===")
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    patronymic = input("Отчество: ")
    passport_number = input("Номер паспорта: ")
    destination_airport = input("Аэропорт назначения: ")
    account_balance = float(input("Баланс счёта (руб.): "))

    # Ввод даты вылета
    while True:
        try:
            date_str = input("Дата вылета (ДД.ММ.ГГГГ): ")
            flight_date = datetime.strptime(date_str, '%d.%m.%Y')
            break
        except ValueError:
            print("Неверный формат даты. Попробуйте снова.")

    return Passenger(
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        passport_number=passport_number,
        destination_airport=destination_airport,
        account_balance=account_balance,
        flight_date=flight_date
    )

def main():
    # Создаём тестовые самолёты
    airplanes = create_sample_airplanes()
    print("\nДоступные рейсы:")
    for i, airplane in enumerate(airplanes, 1):
        print(f"\n{i}. {airplane}")

    # Вводим данные пассажира
    passenger = input_passenger_data()

    # Создаём объект бронирования
    booking = Booking()
    booking.departure_airport = "Москва"  # Аэропорт вылета по умолчанию

    # Осуществляем бронирование
    success = booking.make_booking(passenger, airplanes)

    # Выводим информацию о бронировании
    booking.print_booking_info()

    # Показываем изменения в данных
    print(f"\n=== ИЗМЕНЁННЫЕ ДАННЫЕ ===")
    print(passenger)

    print("\nСостояние самолётов после бронирования:")
    for airplane in airplanes:
        print(f"\n{airplane}")

if __name__ == "__main__":
    main()