import asyncio
import aiohttp
import logging
from time import time
from modules.fetchers import fetch_weather_data, fetch_news_data, fetch_random_users
from modules.excel_writer import save_data_to_excel

logger = logging.getLogger(__name__)


async def main() -> None:
    start = time()
    async with aiohttp.ClientSession() as session:
        weather_task = fetch_weather_data(session)
        news_task = fetch_news_data(session)
        users_task = fetch_random_users(session)
        weather_data, news_data, users_data = await asyncio.gather(
            weather_task, news_task, users_task
        )
    data_fetch_time = time() - start
    save_data_to_excel(weather_data, news_data, users_data)
    data_save_time = time() - start - data_fetch_time
    logger.info(
        f"\n{data_fetch_time:.2f} секунд заняло получение данных.\n"
        f"{data_save_time:.2f} секунд заняло сохранение данных.\n"
        f"{time() - start:.2f} секунд - общее время выполнение скрипта."
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as top_exception:
        logger.exception(f"Unexpected error: {top_exception}")
