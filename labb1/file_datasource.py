from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename

        self.accel_file = None
        self.gps_file = None
        self.parking_file = None

        self.accel_reader = None
        self.gps_reader = None
        self.parking_reader = None

    def read(self) -> AggregatedData:

        # Читаємо по одному рядку з кожного файлу
        accel_row = next(self.accel_reader, None)
        gps_row = next(self.gps_reader, None)
        parking_row = next(self.parking_reader, None)

        # Перевіряємо, чи є дані у файлах
        if accel_row is None or gps_row is None or parking_row is None:
            raise ValueError("No more data in files")

        # Якщо поточний рядок є заголовком, зчитуємо наступний рядок
        while accel_row[0].lower() == 'x':
            accel_row = next(self.accel_reader, None)

        # Якщо залишився тільки заголовок, викидаємо виняток
        if accel_row is None:
            raise ValueError("No more valid data in accelerometer file")

        # Перевіряємо, чи поточний рядок gps_row є заголовком
        if gps_row[0].lower() == 'longitude':
            # Якщо так, зчитуємо наступний рядок
            gps_row = next(self.gps_reader, None)

        # Перевіряємо, чи залишився тільки заголовок, викидаємо виняток
        if gps_row is None:
            raise ValueError("No more valid data in gps file")

        # Перевіряємо, чи поточний рядок parking_row є заголовком
        if parking_row[0].lower() == 'empty_count':
            # Якщо так, зчитуємо наступний рядок
            parking_row = next(self.parking_reader, None)

        # Перевіряємо, чи залишився тільки заголовок, викидаємо виняток
        if parking_row is None:
            raise ValueError("No more valid data in parking file")

        # Створюємо об'єкти Accelerometer та Gps з прочитаних даних (потрібно адаптувати до вашого формату даних)
        accelerometer = Accelerometer(x=int(accel_row[0]), y=int(accel_row[1]), z=int(accel_row[2]))
        gps = Gps(longitude=float(gps_row[0]), latitude=float(gps_row[1]))
        parking = Parking(empty_count=int(parking_row[0]), gps=Gps(float(parking_row[1]), float(parking_row[2])))

        # Повертаємо AggregatedData
        return AggregatedData(accelerometer=accelerometer, gps=gps, parking=parking, timestamp=datetime.now(),
                              user_id=1)

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        # Відкриваємо файли
        self.accel_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.parking_file = open(self.parking_filename, 'r')

        # Створюємо читачі для файлів
        self.accel_reader = reader(self.accel_file)
        self.gps_reader = reader(self.gps_file)
        self.parking_reader = reader(self.parking_file)

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        # Закриваємо файли при закінченні читання
        if self.accel_file:
            self.accel_file.close()
        if self.gps_file:
            self.gps_file.close()
        if self.parking_file:
            self.parking_file.close()
