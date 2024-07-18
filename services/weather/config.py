OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
)

from dataclasses import dataclass
from environs import Env


@dataclass
class OpenWeather:
    api_key: str
    url: str  


@dataclass
class Config:
    weather_service: OpenWeather


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(weather_service=OpenWeather(api_key=env('WEATHER_API'), url=OPENWEATHER_URL))