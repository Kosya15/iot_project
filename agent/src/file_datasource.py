from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename

        self.accelerometer_file = None
        self.gps_file = None
        self.accelerometer_reader = None
        self.gps_reader = None

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        try:
            accelerometer_row = next(self.accelerometer_reader)
            gps_row = next(self.gps_reader)
        except StopIteration:
            self.stopReading()
            self.startReading()
            accelerometer_row = next(self.accelerometer_reader)
            gps_row = next(self.gps_reader)

        accelerometer_data = Accelerometer(
            x=int(accelerometer_row[0]),
            y=int(accelerometer_row[1]),
            z=int(accelerometer_row[2])
        )

        gps_data = Gps(
            longitude=float(gps_row[0]),
            latitude=float(gps_row[1])
        )

        return AggregatedData(
            accelerometer=accelerometer_data,
            gps=gps_data,
            timestamp=datetime.now(),
            user_id=config.USER_ID
        )

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')

        self.accelerometer_reader = reader(self.accelerometer_file)
        self.gps_reader = reader(self.gps_file)

        next(self.accelerometer_reader)
        next(self.gps_reader)

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()
