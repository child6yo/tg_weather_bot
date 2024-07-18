from langchain.schema import SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

from services.gigachain.config import Config, load_config
from services.weather.weather_api_service import Weather

config: Config = load_config()

# Авторизация в сервисе GigaChat
chat = GigaChat(
    credentials=config.chat.credentials,
    model="GigaChat",
    verify_ssl_certs=False,
)



def answer(weather: Weather) -> str:
    city = weather.city
    temperature = weather.temperature
    weather_type = weather.weather_type
    prompt = config.chat.prompt.format(
        city=city, temperature=temperature, weather_type=weather_type
    )
    ans = chat([SystemMessage(content=prompt)])
    return ans.content