from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Какая сейчас погода?"),
            KeyboardButton(text="Прогноз погоды"),
        ],
        [
            KeyboardButton(text="Определить местоположение", request_location=True),
            KeyboardButton(text="Сменить город вручную"),
        ],
        [
            KeyboardButton(text="Сменить стиль ответов"),
        ],
    ],
    resize_keyboard=True,
)

forecast = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Завтра"),
            KeyboardButton(text="Послезавтра"),
        ]
    ],
    resize_keyboard=True,
)

chatstyle = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Русский аристократ (по умолчанию)"),
            KeyboardButton(text="Вор в законе"),
        ]
    ],
    resize_keyboard=True
)