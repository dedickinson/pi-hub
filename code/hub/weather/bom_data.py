import pickle
import os
from os import path
from datetime import datetime

from hub.weather.data_service import WeatherDataService
from hub.weather.model import WeatherStation, WeatherObservation, WeatherForecast, WeatherForecastEntry


# Notes:
# - Icon codes: http://reg.bom.gov.au/info/forecast_icons.shtml

class BomData(WeatherDataService):

    # For list of weather stations, try http://www.bom.gov.au/climate/data/stations/
    __station_list = [
        WeatherStation(
            station_id='040004',
            country='au',
            state='qld',
            name='Amberley',
            latitude=-27.6297,
            longitude=152.7111,
            observation_url='http://reg.bom.gov.au/fwo/IDQ60901/IDQ60901.94568.json',
            forecast_url='ftp://ftp.bom.gov.au/anon/gen/fwo/IDQ11295.xml'
        )
    ]

    def __init__(self, station: WeatherStation,
                 observation_frequency=60, forecast_frequency=30,
                 data_dir=path.expanduser('~/.weather-data/')):
        super().__init__()
        self.station: WeatherStation = station

        self.data_dir: str = os.path.join(data_dir, self.station.station_id)
        if not path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.__latest_observation: WeatherObservation = None
        self.__current_forecast: WeatherForecast = None
        self.observation_frequency: int = observation_frequency
        self.forecast_frequency: int = forecast_frequency

    def __load_current_observations(self):
        import requests
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.station.observation_url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            obs = json_data['observations']['data'][0]

            self.__latest_observation = WeatherObservation(
                station=self.station,
                timestamp=datetime.strptime(obs['local_date_time_full'], '%Y%m%d%H%M%S'),
                temperature_apparent=obs['apparent_t'],
                temperature=obs['air_temp'],
                humidity=obs['rel_hum'],
                wind_dir=obs['wind_dir'],
                wind_speed_kmh=obs['wind_spd_kmh'],
                cloud=obs['cloud'],
                pressure=obs['press'],
                pressure_tend=obs['press_tend'],
                rain=obs['rain_trace'],
                weather=obs['weather']
            )

            with open(self.observation_data_file, 'wb') as f:
                pickle.dump(self.__latest_observation, f, pickle.HIGHEST_PROTOCOL)

    @property
    def current_observations(self) -> WeatherObservation:
        if self.__latest_observation is None and path.exists(self.observation_data_file):
            with open(self.observation_data_file, 'rb') as f:
                self.__latest_observation = pickle.load(f)

        #print((datetime.now() - self.__latest_observation.timestamp).seconds / 60)

        if self.__latest_observation is None or (
                (datetime.now() - self.__latest_observation.timestamp).seconds / 60 >= self.observation_frequency):
            #print("loading")
            self.__load_current_observations()

        return self.__latest_observation

    @property
    def observation_data_file(self) -> str:
        return path.join(self.data_dir, 'observation.pickle')

    @property
    def forecast_data_file(self) -> str:
        return path.join(self.data_dir, 'forecast.pickle')

    def __load_current_forecast(self):
        from defusedxml.ElementTree import parse
        from urllib.request import urlopen
        date_format: str = '%Y-%m-%dT%H:%M:%S%z'

        with urlopen(self.station.forecast_url) as response:
            xml_data = parse(response)

        current_issue = datetime.strptime(xml_data.find('./amoc/issue-time-local').text, date_format)
        next_issue = datetime.strptime(xml_data.find('./amoc/next-routine-issue-time-local').text, date_format)

        forecast = WeatherForecast(
            station=self.station,
            current_issue=current_issue,
            next_issue=next_issue
        )

        forecast_data = xml_data.findall('./forecast/area[@description="Ipswich"]/forecast-period')

        for entry in forecast_data:
            precis = entry.find('./text[@type="precis"]')
            date = datetime.strptime(entry.get('start-time-local'), date_format).date()
            rain_chance = entry.find('./text[@type="probability_of_precipitation"]')
            rain_amount = entry.find('./element[@type="precipitation_range"]')
            temperature_max = entry.find('./element[@type="air_temperature_maximum"]')
            temperature_min = entry.find('./element[@type="air_temperature_minimum"]')
            icon_code = entry.find('./element[@type="icon_code"]')

            forecast_entry = WeatherForecastEntry (
                date=date,
                precis=precis.text if precis is not None else None,
                rain_chance=rain_chance.text if rain_chance is not None else None,
                rain_amount=rain_amount.text if rain_amount is not None else None,
                temperature_max=temperature_max.text if temperature_max is not None else None,
                temperature_min=temperature_min.text if temperature_min is not None else None,
                icon_code=icon_code.text if icon_code is not None else None)

            forecast.entries.append(forecast_entry)

        with open(self.forecast_data_file, 'wb') as f:
            pickle.dump(forecast, f, pickle.HIGHEST_PROTOCOL)

        self.__current_forecast = forecast

    @property
    def current_forecast(self) -> WeatherForecast:
        if self.__current_forecast is None and path.exists(self.forecast_data_file):
            with open(self.forecast_data_file, 'rb') as f:
                self.__current_forecast = pickle.load(f)

        if self.__current_forecast is None or \
                datetime.now(self.__current_forecast.next_issue.tzinfo) > self.__current_forecast.next_issue:
            self.__load_current_forecast()

        return self.__current_forecast

    @staticmethod
    def station_list():
        return BomData.__station_list

    @staticmethod
    def get_station_by_id(station_id: str):
        f = filter(lambda s: s.station_id == station_id, BomData.__station_list)
        return list(f)[0]


if __name__ == "__main__":
    station = BomData.get_station_by_id('040004')
    bom = BomData(station)
    print(bom.current_observations)
    print(bom.current_forecast)
