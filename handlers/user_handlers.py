from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from services.main_service import get_answer
from database import db_manager

router = Router()


# хэндлер на команду /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    user_info = await db_manager.get_user_data(user_id=message.from_user.id)

    if len(user_info) == 0:
        await db_manager.insert_user(
            user_data={
                "user_id": message.from_user.id,
                "full_name": message.from_user.full_name,
                "user_login": message.from_user.username,
                "city": None,
            }
        )
        await message.answer(text=LEXICON_RU["НОВЫЙ ПОЛЬЗОВАТЕЛЬ"])
    else:
        await message.answer(text=LEXICON_RU["СТАРЫЙ ПОЛЬЗОВАТЕЛЬ"])
    
@router.message(Command(commands="weather"))
async def show_weather(message: Message):
    user_info = await db_manager.get_user_data(user_id=message.from_user.id)

    if user_info["city"]:
        try:
            await message.answer(text=get_answer(user_info["city"]))
        except:
            await message.answer(text=LEXICON_RU["ОШИБКА"])
    else:
        await message.answer(text=LEXICON_RU["ОШИБКА ГОРОДА"])

@router.message()
async def change_user_city_and_show_weather(message: Message):
    try:
        await message.answer(text=get_answer(message.text))
        await db_manager.change_user_city(
            user_id=message.from_user.id, city=message.text
        )
    except:
        await message.answer(text=LEXICON_RU["ОШИБКА"])
