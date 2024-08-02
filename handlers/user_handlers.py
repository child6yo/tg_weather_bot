from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from lexicon.lexicon_ru import LEXICON_RU
from services.main_service import get_answer, get_city_from_loc
from database import db_manager
from keyboards import keyboards as kb

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
        await message.answer(
            text=LEXICON_RU["НОВЫЙ ПОЛЬЗОВАТЕЛЬ"], reply_markup=kb.main
        )
    else:
        await message.answer(
            text=LEXICON_RU["СТАРЫЙ ПОЛЬЗОВАТЕЛЬ"], reply_markup=kb.main
        )


@router.message(F.text.lower() == "какая сейчас погода?")
async def show_weather(message: Message):
    user_info = await db_manager.get_user_data(user_id=message.from_user.id)

    if user_info["city"]:
        try:
            await message.answer(text=get_answer(user_info["city"]))
        except:
            await message.answer(text=LEXICON_RU["ОШИБКА"])
    else:
        await message.answer(text=LEXICON_RU["ОШИБКА ГОРОДА"])

@router.message(F.content_type == ContentType.LOCATION)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    city = get_city_from_loc(lat, lon)
    reply = f"Город определен как {city}"
    try:
        await message.answer(reply)
        await db_manager.change_user_city(
        user_id=message.from_user.id, city=city
    )
    except:
        await message.answer(text=LEXICON_RU["ОШИБКА"])


@router.message()
async def change_user_city_and_show_weather(message: Message):
    try:
        await message.answer(text=f"Город изменен на {message.text}")
        await db_manager.change_user_city(
            user_id=message.from_user.id, city=message.text
        )
    except:
        await message.answer(text=LEXICON_RU["ОШИБКА"])
