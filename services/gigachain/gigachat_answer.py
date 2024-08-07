from langchain.schema import SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from services.gigachain.config import Config, load_config
from services.weather.weather_api_service import CurrentWeather, FutureWeather


config: Config = load_config()

# Авторизация в сервисе GigaChat
chat = GigaChat(
    credentials="MDFlNThmMTctZjI1Yi00Yjk0LTg3YzEtYTEyMzEzZjM3MGM2OmFlNWY4MjlhLWY5NGEtNDk4Yy1iZmEwLTUyZDUzOTVhMzg3MQ==",
    model="GigaChat",
    verify_ssl_certs=False,
)


def answer(weather: CurrentWeather) -> str:
    city = weather.city
    temperature = weather.temperature
    weather_type = weather.weather_type
    time = weather.is_day_or_night
    prompt = config.chat.prompt.format(
        city=city, temperature=temperature, weather_type=weather_type, time=time
    )
    ans = chat([SystemMessage(content=prompt)])
    return ans.content


def forecast_answer(weather: FutureWeather) -> str:
    city = weather.city
    max_temp = weather.max_temperature
    min_temp = weather.min_temperature
    weather_type = weather.weather_type
    day = weather.day
    prompt = config.chat.forecast_prompt.format(
        day=day,
        city=city,
        max_temperature=max_temp,
        min_temperature=min_temp,
        weather_type=weather_type,
    )
    ans = chat([SystemMessage(content=prompt)])
    return ans.content
