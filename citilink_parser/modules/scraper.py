from typing import List, Dict, Optional, Tuple, Union
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from .driver import init_driver
import logging

logger = logging.getLogger(__name__)

# Тип для продукта
ProductType = Dict[str, Union[str, float]]


def scrape_page(page_num: int) -> Tuple[int, Optional[List[ProductType]]]:
    """
    Получает HTML-код страницы, дожидаясь появления хотя бы одного заполненного заголовка продукта,
    и возвращает номер страницы и список продуктов.
    """
    base_url = "https://www.citilink.ru/catalog/processory/?ref=undefined&p={}&sorting=price_desc"
    url = base_url.format(page_num)
    logger.info(f"[Страница {page_num}] Обработка URL: {url}")

    driver = None
    html = ""
    try:
        driver = init_driver()
        driver.get(url)
        # Ждем появления хотя бы одного заполненного заголовка продукта
        WebDriverWait(driver, 10).until(
            lambda d: any(
                elem.text.strip()
                for elem in d.find_elements(
                    By.CSS_SELECTOR, "a[data-meta-name='Snippet__title']"
                )
            )
        )
    except TimeoutException:
        logger.warning(
            f"[Страница {page_num}] Время ожидания истекло, заголовки продукта не загрузились вовремя."
        )
    except Exception as e:
        logger.error(f"[Страница {page_num}] Ошибка при загрузке страницы: {e}")
    finally:
        if driver:
            html = driver.page_source
            driver.quit()

    products = parse_products(html)
    return page_num, products


def parse_products(html: str) -> Optional[List[ProductType]]:
    """
    Парсит HTML-страницу для извлечения данных о процессорах.
    Возвращает список словарей с данными провидителя, модели и цены.
    """
    if not html:
        return None
    if "Нет подходящих товаров" in html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    products: List[ProductType] = []
    product_containers = soup.find_all("div", attrs={"data-meta-product-id": True})
    for container in product_containers:
        title_tag = container.find("a", attrs={"data-meta-name": "Snippet__title"})
        if not title_tag:
            continue
        title_text: str = title_tag.get_text(strip=True)
        if not title_text:
            continue

        price_tag = container.find("span", attrs={"data-meta-price": True})
        if not price_tag:
            continue
        price_str: str = price_tag.get("data-meta-price", "0").strip()
        try:
            price: float = float(price_str)
        except ValueError:
            logger.warning(
                f"Не удалось преобразовать цену '{price_str}' в число, используется 0.0"
            )
            price = 0.0

        tokens = title_text.split()
        if tokens and tokens[0].lower() == "процессор" and len(tokens) > 2:
            manufacturer = tokens[1]
            model = " ".join(tokens[2:]).replace(",", "").strip()
        else:
            manufacturer = ""
            model = title_text

        products.append({"Производитель": manufacturer, "Модель": model, "Цена": price})
    return products


def scrape_products_concurrently(batch_size: int = 5) -> List[ProductType]:
    """
    Параллельно собирает данные со страниц с использованием ThreadPoolExecutor.
    Продолжает, пока не встретится страница без товаров.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time

    all_products: List[ProductType] = []
    page_num = 1
    stop_scraping = False

    while not stop_scraping:
        futures = {}
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            for i in range(batch_size):
                current_page = page_num + i
                futures[executor.submit(scrape_page, current_page)] = current_page

            results = []
            for future in as_completed(futures):
                try:
                    current_page, products = future.result()
                    results.append((current_page, products))
                except Exception as e:
                    logger.error(
                        f"Ошибка в выполнении задачи для страницы {futures[future]}: {e}"
                    )

            results.sort(key=lambda x: x[0])
            for current_page, products in results:
                if not products:
                    logger.info(
                        f"[Страница {current_page}] Товары закончились или не найдены."
                    )
                    stop_scraping = True
                    break
                all_products.extend(products)
        page_num += batch_size

    return all_products
