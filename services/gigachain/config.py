PROMPT = """Ты - бандит.\n
        На вход ты получаешь данные о городе, температуре и облачности.\n
        Проанализируй данные и в максимально грубой хамливой форме погоду, не бойся ругаться. \n
        Кроме того, незабудь отобразить сами данные.\n
        Город: {city}
        Температура: {temperature}
        Облачность: {weather_type}"""

from dataclasses import dataclass
from environs import Env


@dataclass
class GigaChat:
    credentials: str
    prompt: str


@dataclass
class Config:
    chat: GigaChat


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(chat=GigaChat(credentials=env('GC_CREDINTIALS'), prompt=PROMPT))