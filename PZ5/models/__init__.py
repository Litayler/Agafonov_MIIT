"""
Подпакет models — содержит основные модели данных системы бронирования:
* Passenger — данные пассажира;
* Airplane — информация о рейсах и самолётах;
* Booking — данные о бронированиях.
"""

from .passenger import Passenger
from .airplane import Airplane
from .booking import Booking

__all__ = [
    'Passenger',
    'Airplane',
    'Booking'
]