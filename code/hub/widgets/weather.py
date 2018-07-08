import threading

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QGridLayout

from hub.weather.bom_data import BomData


class WeatherWidget(QWidget):
    class CurrentTemperature(QLabel):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self.setText('--')
            self.setAlignment(Qt.AlignVCenter)
            self.setObjectName('weather_current_temperature')

        def setText(self, value: str):
            super().setText(f"{value} ℃")

    class GeneralLabel(QLabel):
        def __init__(self, parent: QWidget, name: str):
            super().__init__(parent)
            self.setText('--')
            self.setAlignment(Qt.AlignVCenter)
            self.setObjectName(name)

        def setText(self, value: str):
            super().setText(value)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.temperature_display = WeatherWidget.CurrentTemperature(self)
        self.observation_timestamp = WeatherWidget.GeneralLabel(self, 'observation_timestamp')

        inner_layout_lhs = QVBoxLayout()
        inner_layout_lhs.addWidget(self.temperature_display, alignment=Qt.AlignHCenter)
        inner_layout_lhs.addWidget(self.observation_timestamp, alignment=Qt.AlignHCenter)

        self.observation_weather = WeatherWidget.GeneralLabel(self, 'weather')
        inner_layout_lhs.addWidget(self.observation_weather, alignment=Qt.AlignHCenter)

        observation_data_layout = QGridLayout()
        inner_layout_lhs.addLayout(observation_data_layout)

        self.observation_humidity = WeatherWidget.GeneralLabel(self, 'observation_humidity')
        self.observation_wind = WeatherWidget.GeneralLabel(self, 'observation_wind')
        self.observation_apparent = WeatherWidget.GeneralLabel(self, 'observation_apparent')

        col: int = 0
        for el in ['Humidity', 'Wind', 'Apparent']:
            lbl = QLabel()
            lbl.setText(el)
            observation_data_layout.addWidget(lbl, 0, col, 1, 1, Qt.AlignHCenter)
            col += 1

        observation_data_layout.addWidget(self.observation_humidity, 1, 0, 1, 1, Qt.AlignHCenter)
        observation_data_layout.addWidget(self.observation_wind, 1, 1, 1, 1, Qt.AlignHCenter)
        observation_data_layout.addWidget(self.observation_apparent, 1, 2, 1, 1, Qt.AlignHCenter)

        self.observation_cloud = WeatherWidget.GeneralLabel(self, 'observation_cloud')
        self.observation_pressure = WeatherWidget.GeneralLabel(self, 'observation_pressure')
        self.observation_rain = WeatherWidget.GeneralLabel(self, 'observation_rain')

        col = 0
        for el in ['Cloud', 'Pressure', 'Rain']:
            lbl = QLabel()
            lbl.setText(el)
            observation_data_layout.addWidget(lbl, 2, col, 1, 1, Qt.AlignHCenter)
            col += 1

        observation_data_layout.addWidget(self.observation_cloud, 3, 0, 1, 1, Qt.AlignHCenter)
        observation_data_layout.addWidget(self.observation_pressure, 3, 1, 1, 1, Qt.AlignHCenter)
        observation_data_layout.addWidget(self.observation_rain, 3, 2, 1, 1, Qt.AlignHCenter)


        layout = QHBoxLayout(self)
        layout.addLayout(inner_layout_lhs)
        #layout.addLayout(inner_layout_rhs)
        self.setLayout(layout)

        # Break this out into a more centralised approach
        self.weather_data = BomData(BomData.get_station_by_id('040004'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__update_weather)
        self.timer.start(60000)
        # This looks ok - just read up on it
        # See also http://doc.qt.io/qt-5/thread-basics.html
        thread = threading.Thread(target=self.__update_weather, args=())
        thread.start()

    def __update_weather(self):
        current_obs = self.weather_data.current_observations
        self.temperature_display.setText(f"{current_obs.temperature}")
        self.observation_timestamp.setText(current_obs.timestamp.strftime("%d/%m/%Y %H:%M"))
        self.observation_humidity.setText(f"{current_obs.humidity}%")
        self.observation_wind.setText(f"{current_obs.wind_speed_kmh}km/h {current_obs.wind_dir}")
        self.observation_apparent.setText(f"{current_obs.temperature_apparent} ℃")
        self.observation_weather.setText(f"{current_obs.weather}")
        self.observation_cloud.setText(f"{current_obs.cloud}")
        self.observation_pressure.setText(f"{current_obs.pressure} {current_obs.pressure_tend}")
        self.observation_rain.setText(f"{current_obs.rain}")
