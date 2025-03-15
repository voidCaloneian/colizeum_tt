from typing import Any
import time
import logging
from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone
from .models import CSVFile

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_csv_file(self: Any, csv_file_id: int) -> str:
    """
    Обработка CSV файла
    """
    try:
        csv_file: CSVFile = CSVFile.objects.get(
            id=csv_file_id
        )  # pylint: disable=no-member
        csv_file.status = "processing"
        csv_file.save()

        # Имитируем длительную обработку (sleep 60)
        time.sleep(60)

        # Здесь должна быть логика обработки CSV. Для примера результат фиксированный:
        result: str = "CSV processed successfully."
        csv_file.result = result
        csv_file.status = "completed"
        csv_file.processed_at = timezone.now()
        csv_file.save()

        # Отправляем email с уведомлением
        subject: str = "Ваш CSV файл обработан"
        message: str = (
            f"Здравствуйте,\n\nВаш CSV файл (ID: {csv_file.id}) успешно обработан.\nРезультат: {result}"
        )
        EmailMessage(
            subject=subject,
            body=message,
            to=[csv_file.email],
        ).send()

        return "CSV обработан успешно"
    except Exception as exc:
        logger.error(f"Ошибка обработки CSV файла ID {csv_file_id}: {exc}")
        csv_file: CSVFile = CSVFile.objects.get(
            id=csv_file_id
        )  # pylint: disable=no-member
        csv_file.status = "error"
        csv_file.save()
        self.retry(exc=exc)
