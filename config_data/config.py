from dataclasses import dataclass
from environs import Env


@dataclass
class GigaChat:
    credentials: str


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Postgres:
    source: str
    password: str


@dataclass
class Config:
    tg_bot: TgBot
    database: Postgres
    chat: GigaChat


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        database=Postgres(
            source=env("POSTGRES_SOURCE"),
            password=env("POSTGRES_PASSWORD"),
        ),
        chat=GigaChat(credentials=env("GC_CREDINTIALS")),
    )
