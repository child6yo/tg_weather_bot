from typing import NamedTuple
from services.weather.weather_codes import WEATHER_CODES
import requests

Celsius = int


class CurrentWeather(NamedTuple):
    temperature: Celsius
    weather_type: str
    city: str
    is_day_or_night: str


class FutureWeather(NamedTuple):
    day: str
    weather_type: str
    max_temperature: str
    min_temperature: str
    city: str


class Coordinates(NamedTuple):
    latitude: str
    longtitude: str


class WeatherService:

    def get_city_coordinates(self, city_name: str) -> Coordinates:
        data = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru&format=json"
        ).json()
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        return Coordinates(latitude=lat, longtitude=lon)

    def get_current_weather(self, city_name: str) -> CurrentWeather:
        coordinates = self.get_city_coordinates(city_name)
        weather_data = self.__current_weather_parcer(coordinates)
        formated_weather = self.__current_weather_formater(weather_data, city_name)
        return formated_weather

    def get_forecast(self, city_name: str, day: int) -> FutureWeather:
        coordinates = self.get_city_coordinates(city_name)
        forecast_data = self.__forecast_parcer(coordinates)
        formated_forecast = self.__forecast_formater(forecast_data, city_name, day)
        return formated_forecast

    def __current_weather_parcer(self, coordinates: Coordinates) -> dict:
        lat = coordinates.latitude
        lon = coordinates.longtitude
        weather_data = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,is_day,weather_code"
        ).json()
        return weather_data

    def __forecast_parcer(self, coordinates: Coordinates) -> dict:
        lat = coordinates.latitude
        lon = coordinates.longtitude
        forecast_data = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min"
        ).json()
        return forecast_data

    def __current_weather_formater(
        self, weather_data: dict, city_name: str
    ) -> CurrentWeather:
        temperature = int(weather_data["current"]["temperature_2m"])
        w_type = WEATHER_CODES[int(weather_data["current"]["weather_code"])]
        city = city_name
        is_day = bool(weather_data["current"]["is_day"])
        is_day_or_night = "День" if is_day else "Ночь"
        return CurrentWeather(
            temperature=temperature,
            weather_type=w_type,
            city=city,
            is_day_or_night=is_day_or_night,
        )

    def __forecast_formater(
        self, forecast_data: dict, city_name: str, day: int
    ) -> FutureWeather:
        current_day = forecast_data["daily"]["time"][day]
        w_type = WEATHER_CODES[int(forecast_data["daily"]["weather_code"][day])]
        max_temp = forecast_data["daily"]["temperature_2m_max"][day]
        min_temp = forecast_data["daily"]["temperature_2m_min"][day]
        city = city_name
        return FutureWeather(
            day=current_day,
            weather_type=w_type,
            max_temperature=max_temp,
            min_temperature=min_temp,
            city=city,
        )
