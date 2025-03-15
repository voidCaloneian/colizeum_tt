import aiohttp
import asyncio
from typing import Any, Dict, List, Optional
from .config import config
from .utils import get_data_from_api
from .cities import CITIES
import logging

logger = logging.getLogger(__name__)


async def fetch_weather_for_city(
    session: aiohttp.ClientSession, city: str
) -> Optional[Dict[str, Any]]:
    """Запрашиваем данные о погоде для конкретного города"""
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={config['OPENWEATHER_API_KEY']}&units=metric"
    )
    data = await get_data_from_api(
        session,
        url,
        error_context=f"Weather request error for {city}",  # Возникает, если ваш API ключ неверный, либо
        validator=lambda d: str(d.get("cod")) == "200",  # Не успел еще активироваться!
    )
    return data


async def fetch_weather_data(session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
    """
    Запрашиваем данные о погоде для всех городов из списка CITIES
    """
    logger.info("[Погода] Запрашиваем данные о погоде.")
    tasks = [fetch_weather_for_city(session, city) for city in CITIES]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # Если ошибка в одном из запросов, выводим сообщение
    if any(result is None for result in results):
        logger.critical(
            "Не удалось обратиться к погодному API, либо ваш ключ невалидный, либо не успел еще активироваться!"
        )
        return []
    logger.info("[Погода] Данные о погоде успешно получены.")
    return [result for result in results if isinstance(result, dict) and result]


async def fetch_news_data(session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
    """
    Запрашиваем данные о новостях по теме PC gaming
    """
    logger.info("[Новости] Запрашиваем данные о новостях.")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=PC+gaming&apikey={config['NEWSAPI_API_KEY']}&language=en&pageSize=50"
    )
    logger.info("[Новости] Данные о новостях успешно получены.")
    return await get_data_from_api(
        session, url, "NewsAPI request error", extraction_key="articles"
    )


async def fetch_random_users(
    session: aiohttp.ClientSession, results_count: int = 50
) -> List[Dict[str, Any]]:
    """
    Запрашиваем данные о случайных пользователях
    """
    logger.info("[Пользователи] Запрашиваем данные о случайных пользователях.")
    url = f"https://randomuser.me/api/?results={results_count}"

    logger.info("[Пользователи] Данные о пользователях успешно получены.")
    return await get_data_from_api(
        session, url, "RandomUser API request error", extraction_key="results"
    )
