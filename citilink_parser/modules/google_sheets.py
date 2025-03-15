import requests
import time
import logging
import pandas as pd
from typing import List

logger = logging.getLogger(__name__)


def update_google_sheets(
    data_df: pd.DataFrame,
    spreadsheet_id: str,
    sheet_name: str,
    token: str,
    retry: int = 3,
) -> None:
    """
    Обновляет данные в Google Sheets через API.
    Пытается выполнить запрос до 'retry' раз в случае неудачи.
    """
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_name}:append?valueInputOption=RAW"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Формируем payload: первая строка – заголовки, затем данные
    values: List[List[str]] = [data_df.columns.tolist()] + data_df.astype(
        str
    ).values.tolist()
    payload = {"values": values}

    attempt = 0
    while attempt < retry:
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                logger.info("Данные успешно обновлены в Google Sheets.")
                return
            else:
                logger.error(
                    f"Попытка {attempt + 1}: Ошибка обновления Google Sheets - {response.text}"
                )
        except requests.RequestException as e:
            logger.error(
                f"Попытка {attempt + 1}: Исключение при запросе обновления Google Sheets - {e}"
            )
        attempt += 1
        time.sleep(2)
    logger.error("Не удалось обновить данные в Google Sheets после нескольких попыток.")
