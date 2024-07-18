from services.weather.weather_api_service import get_weather
from services.gigachain.gigachat_answer import answer

def get_answer(user_input: str) -> str:
    weather = get_weather(user_input)
    llm_answer = answer(weather)
    return llm_answer

