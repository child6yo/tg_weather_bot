from typing import NamedTuple
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


weather_codes = {
    0: "Ясно",
    1: "В основном ясно",
    2: "Частично облачно",
    3: "Облачно",
    45: "Туман",
    48: "Холодный туман",
    51: "Морось",
    53: "Мелкий дождь",
    55: "Плотная морось",
    56: "Морозящая морось",
    57: "Морозящая морось",
    61: "Небольшой дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    66: "Холодный дождь",
    67: "Сильный холодный дождь",
    71: "Слабый снегопад",
    73: "Средний снегопад",
    75: "Сильный снегопад",
    77: "Снежные крупинки",
    80: "Легкий ливень",
    81: "Средний ливень",
    82: "Сильный ливень",
    85: "Небольшая снежная буря",
    86: "Снежная буря",
    95: "Гроза",
    96: "Грозовой шторм",
}


def get_city_coordinates(city_name: str) -> Coordinates:
    data = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru&format=json"
    ).json()
    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    return Coordinates(latitude=lat, longtitude=lon)


def get_current_weather(city_name: str) -> CurrentWeather:
    coordinates = get_city_coordinates(city_name)
    weather_data = current_weather_parcer(coordinates)
    temperature = int(weather_data["current"]["temperature_2m"])
    w_type = weather_codes[int(weather_data["current"]["weather_code"])]
    city = city_name
    is_day = bool(weather_data["current"]["is_day"])
    is_day_or_night = "День" if is_day else "Ночь"
    return CurrentWeather(
        temperature=temperature,
        weather_type=w_type,
        city=city,
        is_day_or_night=is_day_or_night,
    )


def get_forecast(city_name: str, day: int) -> FutureWeather:
    coordinates = get_city_coordinates(city_name)
    forecast_data = forecast_parcer(coordinates)
    current_day = forecast_data["daily"]["time"][day]
    w_type = weather_codes[int(forecast_data["daily"]["weather_code"][day])]
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


def current_weather_parcer(coordinates: Coordinates) -> dict:
    lat = coordinates.latitude
    lon = coordinates.longtitude
    weather_data = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,is_day,weather_code"
    ).json()
    return weather_data


def forecast_parcer(coordinates: Coordinates) -> dict:
    lat = coordinates.latitude
    lon = coordinates.longtitude
    forecast_data = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min"
    ).json()
    return forecast_data
