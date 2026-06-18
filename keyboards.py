from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

POPULAR_CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Минск", "Алматы", "Киев"]


def cities_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=city, callback_data=f"city:{city}")
        for city in POPULAR_CITIES
    ]
    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def location_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Отправить геолокацию", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
