from datetime import datetime, date
from dataclasses import dataclass, field
from typing import List


@dataclass
class WeatherStation:
    station_id: str
    country: str
    state: str
    name: str
    latitude: float
    longitude: float
    observation_url: str
    forecast_url: str


@dataclass
class WeatherObservation:
    station: WeatherStation
    timestamp: datetime
    temperature_apparent: float
    temperature: float
    humidity: int
    wind_dir: str
    wind_speed_kmh: int
    cloud: str
    pressure: float
    pressure_tend: str
    rain: float
    weather: str

@dataclass
class WeatherForecastEntry:
    precis: str = None
    date: date = None
    rain_chance: str = None
    rain_amount: str = None
    temperature_max: int = None
    temperature_min: int = None
    icon_code: int = None


@dataclass
class WeatherForecast:
    station: WeatherStation
    current_issue: datetime
    next_issue: datetime
    entries: List[WeatherForecastEntry] = field(default_factory=list)
