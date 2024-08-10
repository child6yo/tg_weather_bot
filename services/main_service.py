from services.weather.weather_api_service import WeatherService
from langchain_community.chat_models.gigachat import GigaChat
from services.gigachain.gigachat_answer import Chat
from geopy.geocoders import Nominatim
from config_data.config import Config, load_config
from services.gigachain.prompts import PROMPTS

config: Config = load_config()

weather_service = WeatherService()

generative_model = GigaChat(
    credentials=config.chat.credentials,
    model="GigaChat",
    verify_ssl_certs=False,
)


class AnswerService:

    def __init__(self, chat_style: str) -> None:
        self.chat = Chat(
            generative_model, PROMPTS[chat_style], PROMPTS["FUT_" + chat_style]
        )

    def get_answer(self, city_name: str) -> str:
        weather = weather_service.get_current_weather(city_name)
        llm_answer = self.chat.answer(weather)
        return llm_answer

    def get_forecast_answer(self, city_name: str, day: int) -> str:
        weather = weather_service.get_forecast(city_name, day)
        llm_answer = self.chat.forecast_answer(weather)
        return llm_answer


class LocationService:

    def get_city_from_loc(self, lat: str, lon: str) -> str:
        geolocator = Nominatim(user_agent="WeatherService")
        location = geolocator.reverse(f"{lat}, {lon}")
        return str(location.raw["address"]["city"])
