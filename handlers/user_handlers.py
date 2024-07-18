from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from services.main_service import get_answer
from transliterate import translit

import urllib.error

router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

# Этот хэндлер срабатывает на все остальные сообщения и обращается к погодному сервису
@router.message()
async def send_current_weather(message: Message):
    latin_message = translit(message.text, language_code='ru', reversed=True)
    try:
       await message.answer(text=get_answer(latin_message))
    except urllib.error.HTTPError:
       await message.answer(text=LEXICON_RU['ОШИБКА НАЗВАНИЯ'])
    except UnicodeEncodeError:
        await message.answer(text=LEXICON_RU['ОШИБКА ЯЗЫКА'])