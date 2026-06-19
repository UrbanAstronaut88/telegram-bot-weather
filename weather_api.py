import aiohttp

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

WEATHER_EMOJI = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧",
    "Drizzle": "🌦",
    "Thunderstorm": "⛈",
    "Snow": "❄️",
    "Mist": "🌫",
    "Fog": "🌫",
    "Haze": "🌫",
}


class WeatherError(Exception):
    """Базовая ошибка при получении погоды."""


class CityNotFoundError(WeatherError):
    """Город с таким названием не найден."""


async def _request(params: dict, api_key: str) -> dict:
    query = {**params, "appid": api_key, "units": "metric", "lang": "ru"}
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(BASE_URL, params=query) as resp:
            data = await resp.json()
            if resp.status == 404:
                raise CityNotFoundError(data.get("message", "Город не найден"))
            if resp.status != 200:
                raise WeatherError(data.get("message", f"Ошибка API: {resp.status}"))
            return data


async def get_weather_by_city(city: str, api_key: str) -> dict:
    data = await _request({"q": city}, api_key)
    return _parse(data)


async def get_weather_by_coords(lat: float, lon: float, api_key: str) -> dict:
    data = await _request({"lat": lat, "lon": lon}, api_key)
    return _parse(data)


def _parse(data: dict) -> dict:
    weather_main = data["weather"][0]["main"]
    return {
        "city": data["name"],
        "country": data.get("sys", {}).get("country", ""),
        "temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "humidity": data["main"]["humidity"],
        "emoji": WEATHER_EMOJI.get(weather_main, "🌡"),
    }


def format_weather(w: dict) -> str:
    location = f"{w['city']}, {w['country']}" if w["country"] else w["city"]
    return (
        f"{w['emoji']} Погода в городе {location}\n\n"
        f"🌡 Температура: {w['temp']}°C\n"
        f"🤔 Ощущается как: {w['feels_like']}°C\n"
        f"📝 Описание: {w['description']}\n"
        f"💨 Скорость ветра: {w['wind_speed']} м/с\n"
        f"💧 Влажность: {w['humidity']}%"
    )
