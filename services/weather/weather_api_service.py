from typing import NamedTuple
from services.weather.config import Config, load_config
import urllib.request, json

config: Config = load_config()

Celsius = int


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: str
    city: str


def get_weather(city_name: str) -> Weather:
    weather_data = weather_parcer(city_name)
    temp = int(weather_data["main"]["temp"])
    w_type = str(weather_data["weather"][0]["description"])
    place = str(weather_data["name"])
    return Weather(temperature=temp, weather_type=w_type, city=place)


def weather_parcer(city_name: str) -> dict:
    openweather_api = config.weather_service.api_key
    openweather_url = config.weather_service.url.format(
        city=city_name, api_key=openweather_api
    )
    with urllib.request.urlopen(openweather_url) as url:
        weather_data = json.load(url)
    return weather_data
