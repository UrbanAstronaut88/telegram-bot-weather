import os
from dotenv import load_dotenv

load_dotenv()  # читает .env файл, если он есть

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWM_API_KEY = os.getenv("OWM_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError(
        "Не задан BOT_TOKEN. Создайте файл .env по образцу ..env "
        "и впишите туда токен бота от @BotFather."
    )
if not OWM_API_KEY:
    raise RuntimeError(
        "Не задан OWM_API_KEY. Создайте файл .env по образцу ..env "
        "и впишите туда ключ от OpenWeatherMap (https://openweathermap.org/api)."
    )