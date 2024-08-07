from services.weather.weather_api_service import get_current_weather, get_forecast
from services.gigachain.gigachat_answer import answer, forecast_answer
from geopy.geocoders import Nominatim


def get_answer(city_name: str) -> str:
    weather = get_current_weather(city_name)
    llm_answer = answer(weather)
    return llm_answer


def get_forecast_answer(city_name: str, day: int) -> str:
    weather = get_forecast(city_name, day)
    llm_answer = forecast_answer(weather)
    return llm_answer


def get_city_from_loc(lat: str, lon: str) -> str:
    geolocator = Nominatim(user_agent="WeatherService")
    location = geolocator.reverse(f"{lat}, {lon}")
    return str(location.raw["address"]["city"])