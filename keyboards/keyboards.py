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
    "Завтра",
    "Послезавтра",
]

def reply_forecast():
    keyboard = ReplyKeyboardBuilder()
    for day in forecast:
        keyboard.add(KeyboardButton(text=day))
    return keyboard.adjust(2).as_markup()