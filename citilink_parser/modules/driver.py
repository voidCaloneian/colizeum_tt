from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
import logging

logger = logging.getLogger(__name__)


def init_driver() -> WebDriver:
    """
    Инициализация Selenium WebDriver в headless-режиме.
    Возвращает экземпляр драйвера.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("log-level=3")  # Минимизация логов Chrome
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except WebDriverException as e:
        logger.error(f"Ошибка инициализации драйвера: {e}")
        raise e
    return driver
