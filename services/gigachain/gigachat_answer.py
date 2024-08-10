from langchain.schema import SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from services.weather.weather_api_service import CurrentWeather, FutureWeather



class Chat:

    def __init__(self, chat_type: GigaChat, prompt: str, forecast_prompt: str) -> None:
        self.generative_model = chat_type
        self.prompt = prompt
        self.forecast_prompt = forecast_prompt

    def answer(self, weather: CurrentWeather) -> str:
        prompt = self.prompt.format(
            city=weather.city,
            temperature=weather.temperature,
            weather_type=weather.weather_type,
            time=weather.is_day_or_night,
        )
        ans = self.generative_model([SystemMessage(content=prompt)])
        return ans.content

    def forecast_answer(self, weather: FutureWeather) -> str:
        prompt = self.forecast_prompt.format(
            day=weather.day,
            city=weather.city,
            max_temperature=weather.max_temperature,
            min_temperature=weather.min_temperature,
            weather_type=weather.weather_type,
        )
        ans = self.generative_model([SystemMessage(content=prompt)])
        return ans.content
