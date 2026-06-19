import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN, OWM_API_KEY
from weather_api import (
    get_weather_by_city,
    get_weather_by_coords,
    format_weather,
    CityNotFoundError,
    WeatherError,
)
from keyboards import cities_keyboard, location_keyboard

logging.basicConfig(level=logging.INFO)
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я подскажу текущую погоду в любом городе.\n\n"
        "Просто напишите название города текстом, выберите один из "
        "популярных ниже, либо пришлите геолокацию — и я отвечу погодой.",
        reply_markup=location_keyboard(),
    )
    await message.answer("Популярные города:", reply_markup=cities_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Как пользоваться:\n"
        "• Напишите название города (например, «Казань»)\n"
        "• Или нажмите на кнопку с городом\n"
        "• Или отправьте геолокацию через скрепку → Локация"
    )


@router.message(F.location)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    await send_weather_by_coords(message, lat, lon)


@router.callback_query(F.data.startswith("city:"))
async def handle_city_button(callback: CallbackQuery):
    city = callback.data.split(":", 1)[1]
    await callback.answer()
    await send_weather_by_city(callback.message, city)


@router.message(F.text)
async def handle_city_text(message: Message):
    city = message.text.strip()
    await send_weather_by_city(message, city)


async def send_weather_by_city(message: Message, city: str):
    try:
        weather = await get_weather_by_city(city, OWM_API_KEY)
        await message.answer(format_weather(weather))
    except CityNotFoundError:
        await message.answer(
            f"Не нашёл город «{city}». Проверьте написание и попробуйте ещё раз."
        )
    except WeatherError as e:
        await message.answer(f"Не получилось получить погоду: {e}")
    except Exception:
        logging.exception("Unexpected error")
        await message.answer("Что-то пошло не так. Попробуйте позже.")


async def send_weather_by_coords(message: Message, lat: float, lon: float):
    try:
        weather = await get_weather_by_coords(lat, lon, OWM_API_KEY)
        await message.answer(format_weather(weather))
    except WeatherError as e:
        await message.answer(f"Не получилось получить погоду: {e}")
    except Exception:
        logging.exception("Unexpected error")
        await message.answer("Что-то пошло не так. Попробуйте позже.")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())