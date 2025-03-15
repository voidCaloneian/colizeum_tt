from typing import List, Dict, Any
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def save_data_to_excel(
    weather_data: List[Dict[str, Any]],
    news_data: List[Dict[str, Any]],
    users_data: List[Dict[str, Any]],
    filename: str = "data.xlsx",
) -> None:
    """
    Сохраняем данные в Excel-файл
    """
    weather_records = [
        {
            "City": data.get("name"),
            "Temperature": data.get("main", {}).get("temp"),
            "Weather": (data.get("weather") or [{}])[0].get("description"),
            "Humidity": data.get("main", {}).get("humidity"),
            "Wind Speed": data.get("wind", {}).get("speed"),
        }
        for data in weather_data
    ]
    df_weather = pd.DataFrame(weather_records)
    df_news = pd.DataFrame(news_data)
    df_users = pd.DataFrame(users_data)

    try:
        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            df_weather.to_excel(writer, sheet_name="Weather", index=False)
            df_news.to_excel(writer, sheet_name="News", index=False)
            df_users.to_excel(writer, sheet_name="RandomUsers", index=False)
        logger.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logger.exception(f"Failed to save data to Excel: {e}")
