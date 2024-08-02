from services.weather.weather_api_service import get_weather
from services.gigachain.gigachat_answer import answer
from geopy.geocoders import Nominatim


def get_answer(user_input: str) -> str:
    weather = get_weather(user_input)
    llm_answer = answer(weather)
    return llm_answer

def get_city_from_loc(lat: str, lon: str) -> str:
    geolocator = Nominatim(user_agent="WeatherService")
    location = geolocator.reverse(f"{lat}, {lon}")
    return str(location.raw["address"]["city"])