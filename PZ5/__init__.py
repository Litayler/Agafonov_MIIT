"""
Пакет air_booking — система бронирования авиабилетов.

Содержит подпакеты и модули для работы с пассажирами, самолётами и бронированиями.
"""

__version__ = "1.0.0"
__author__ = "Разработчик системы бронирования"

# Экспорт ключевых классов для удобного импорта
from .models.passenger import Passenger
from .models.airplane import Airplane
from .models.booking import Booking

# Определение публичного API пакета
__all__ = ["Passenger", "Airplane", "Booking"]
