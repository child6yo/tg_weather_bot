from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import  FSMContext
from lexicon.lexicon_ru import LEXICON_RU, CHAT_STYLES
from services.main_service import AnswerService, LocationService
from database import db_manager
from keyboards import keyboards as kb

router = Router()

class UserData(StatesGroup):
    city = State()
    chat_style = State()

class Forecast(StatesGroup):
    day = State()

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
                "chat_style": "ARISTOCRAT"
            }
        )
        await message.answer(
            text=LEXICON_RU["НОВЫЙ ПОЛЬЗОВАТЕЛЬ"], reply_markup=kb.main
        )
    else:
        await message.answer(
            text=LEXICON_RU["СТАРЫЙ ПОЛЬЗОВАТЕЛЬ"], reply_markup=kb.main
        )


# хендлер на кнопку/текст "какая сейчас погода?"
@router.message(F.text.lower() == "какая сейчас погода?")
async def show_weather(message: Message):
    user_info = await db_manager.get_user_data(user_id=message.from_user.id)
    service = AnswerService(user_info["chat_style"])
    try:
        await message.answer(text=service.get_answer(user_info["city"]), reply_markup=kb.main)
    except:
            await message.answer(text=LEXICON_RU["ОШИБКА"], reply_markup=kb.main)

@router.message(F.text.lower() == "прогноз погоды")
async def weather_forecast(message: Message, state: FSMContext):
    user_info = await db_manager.get_user_data(user_id=message.from_user.id)
    if user_info["city"]:
        await state.set_state(Forecast.day)
        await message.answer(text="Прогноз на какой день вас интересует?", reply_markup=kb.forecast)
    else:
        await message.answer(text=LEXICON_RU["ОШИБКА ГОРОДА"], reply_markup=kb.main)

@router.message(Forecast.day)
async def forecast(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    user_info = await db_manager.get_user_data(user_id=message.from_user.id)
    service = AnswerService(user_info["chat_style"])
    if data["name"].lower() == "завтра":
        try:
            await message.answer(text=service.get_forecast_answer(user_info["city"], 1), reply_markup=kb.main)
        except:
            await message.answer(text=LEXICON_RU["ОШИБКА"], reply_markup=kb.main)
    elif data["name"].lower() == "послезавтра":
        try:
            await message.answer(text=service.get_forecast_answer(user_info["city"], 2), reply_markup=kb.main)
        except:
            await message.answer(text=LEXICON_RU["ОШИБКА"], reply_markup=kb.main)
    await state.clear()

@router.message(F.text.lower() == "сменить город вручную")
async def change_user_city(message: Message, state: FSMContext):
    await state.set_state(UserData.city)
    await message.answer(text="Введите город", reply_markup=kb.main)

@router.message(UserData.city)
async def changing_city(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    try:
        await message.answer(text=f"Город изменен на {data["name"]}", reply_markup=kb.main)
        await db_manager.change_user_city(
            user_id=message.from_user.id, city=data["name"]
        )
    except:
        await message.answer(text=LEXICON_RU["ОШИБКА"], reply_markup=kb.main)
    await state.clear()

@router.message(F.text.lower() == "сменить стиль ответов")
async def change_user_chatstyle(message: Message, state: FSMContext):
    await state.set_state(UserData.chat_style)
    await message.answer(text="Выберите стиль чата", reply_markup=kb.chatstyle)

@router.message(UserData.chat_style)
async def changing_chatstyle(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    style: str = data["name"]
    await message.answer(text=f"Стиль чата изменен на {style}", reply_markup=kb.main)
    await db_manager.change_user_chat_style(
        user_id=message.from_user.id, chat_style=CHAT_STYLES[style.upper()]
        )
    await state.clear()


# хендлер на геолокацию
@router.message(F.content_type == ContentType.LOCATION)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    service = LocationService()
    city = service.get_city_from_loc(lat, lon)
    reply = f"Город определен как {city}"
    try:
        await message.answer(reply, reply_markup=kb.main)
        await db_manager.change_user_city(user_id=message.from_user.id, city=city)
    except:
        await message.answer(text=LEXICON_RU["ОШИБКА"], reply_markup=kb.main)

# хендлер на весь остальной текст
@router.message(F.content_type == ContentType.ANY)
async def change_user_city_and_show_weather(message: Message):
    await message.answer(text=LEXICON_RU["ОСТАЛЬНОЕ"], reply_markup=kb.main)
