import logging
from dotenv import dotenv_values

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из файла .env
config = dotenv_values(".env")
SPREADSHEET_ID = config.get("SPREADSHEET_ID")
SHEET_NAME = config.get("SHEET_NAME")
ACCESS_TOKEN = config.get("ACCESS_TOKEN")
