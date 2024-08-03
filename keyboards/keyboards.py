from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Какая сейчас погода?"),
            KeyboardButton(text="Прогноз погоды"),
        ],
        [
            KeyboardButton(text="Определить местоположение", request_location=True),
            KeyboardButton(text="Сменить город вручную"),
        ]
    ],
    resize_keyboard=True,
)

forecast = [
    "1 час",
    "2 часа",
    "3 часа",
    "4 часа",
    "5 часов",
    "6 часов",
    "7 часов",
    "8 часов",
    "9 часов",
    "10 часов",
    "11 часов",
    "12 часов"
]

async def reply_forecast():
    keyboard = ReplyKeyboardBuilder()
    for hour in forecast:
        keyboard.add(KeyboardButton(text=hour))
    return keyboard.adjust(8).as_markup()