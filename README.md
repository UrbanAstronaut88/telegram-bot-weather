# Telegram-бот прогноза погоды

Бот на aiogram 3.x: присылаете название города или геолокацию — получаете
текущую температуру, скорость ветра и описание погоды.

## Установка
``` bash
git clone https://github.com/UrbanAstronaut88/telegram-bot-weather.git
cd telegram-bot-weather
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
 ```
## Настройка

1. Получите токен бота у [@BotFather](https://t.me/BotFather) (команда `/newbot`).
2. Получите бесплатный API-ключ на [openweathermap.org](https://openweathermap.org/api)
   (раздел Current Weather Data). Ключ активируется обычно в течение 10–120 минут
   после регистрации.
3. Скопируйте .env.example в .env и введите ключи:
###### BOT_TOKEN=*******************************
###### OWM_API_KEY=******************************

## Запуск
``` Bash
python main.py
```
Бот начнёт опрашивать Telegram (long polling). Откройте бота в Telegram и
нажмите /start.

## Структура проекта

- main.py — точка входа, хендлеры команд и сообщений
- weather_api.py — запросы к OpenWeatherMap, парсинг JSON, обработка ошибок
- keyboards.py — инлайн-кнопки с городами и кнопка геолокации
- config.py — загрузка токенов из .env

## Что можно добавить дальше

- Кэширование запросов (чтобы не дёргать API повторно для одного города)
- Прогноз на несколько дней вперёд (эндпоинт `/forecast`)
- Сохранение последнего города пользователя (SQLite) и команду /again
- Деплой на сервер (например, PythonAnywhere, VPS + systemd, или Railway) —
  через webhook вместо long polling для продакшна