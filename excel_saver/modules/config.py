import logging
from dotenv import dotenv_values

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
config = dotenv_values(".env")

# Проверяем обязательные ключи
REQUIRED_KEYS = ["OPENWEATHER_API_KEY", "NEWSAPI_API_KEY"]

for key in REQUIRED_KEYS:
    if key not in config or not config[key]:
        raise ValueError(f"Missing mandatory configuration key: {key}")
