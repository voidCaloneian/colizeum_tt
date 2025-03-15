import pandas as pd
from modules.config import SPREADSHEET_ID, SHEET_NAME, ACCESS_TOKEN, logger
from modules.scraper import scrape_products_concurrently
from modules.google_sheets import update_google_sheets


def main() -> None:
    """
    Точка входа в программу.
    Собирает данные о процессорах, сортирует их и обновляет таблицу в Google Sheets.
    """
    products = scrape_products_concurrently(batch_size=5)
    if not products:
        logger.info("Не удалось собрать данные о процессорах.")
        return

    sorted_products = sorted(products, key=lambda x: x["Цена"], reverse=True)
    df = pd.DataFrame(sorted_products)
    logger.info("Результирующая таблица:")
    logger.info("\n" + df.to_string(index=False))

    if SPREADSHEET_ID and SHEET_NAME and ACCESS_TOKEN:
        update_google_sheets(df, SPREADSHEET_ID, SHEET_NAME, ACCESS_TOKEN)
    else:
        logger.error(
            "Отсутствуют необходимые переменные окружения для обновления Google Sheets."
        )


if __name__ == "__main__":
    main()
