import asyncio
import logging
from typing import Any, Dict, Optional, Callable
import aiohttp

logger = logging.getLogger(__name__)


async def fetch_json(
    session: aiohttp.ClientSession, url: str, error_context: str, timeout: int = 10
) -> Optional[Dict[str, Any]]:
    """
    Загружаем JSON с указанного URL
    """
    try:
        async with session.get(url, timeout=timeout) as response:
            if response.status != 200:
                logger.error(f"{error_context} - HTTP {response.status} for URL: {url}")
                return None
            return await response.json()
    except asyncio.TimeoutError:
        logger.error(f"{error_context} - Timeout while requesting URL: {url}")
    except Exception as e:
        logger.exception(f"{error_context} - Exception for URL: {url}: {e}")
    return None


async def get_data_from_api(
    session: aiohttp.ClientSession,
    url: str,
    error_context: str,
    extraction_key: Optional[str] = None,
    validator: Optional[Callable[[Dict[str, Any]], bool]] = None,
) -> Any:
    """
    Получаем данные из API и валидируем их
    """
    data = await fetch_json(session, url, error_context)
    if not data:
        return [] if extraction_key else None
    if validator and not validator(data):
        logger.error(
            f"{error_context} - API response validation failed for URL: {url} with response: {data}"
        )
        return [] if extraction_key else None
    return data.get(extraction_key, []) if extraction_key else data
