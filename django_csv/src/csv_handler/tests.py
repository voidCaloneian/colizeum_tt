from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CSVFile


class CSVFileUploadTest(APITestCase):
    """
    Тесты для загрузки CSV файла
    """

    def test_upload_csv(self) -> None:
        """
        Тест загрузки CSV файла
        """
        url = reverse("csv-upload")
        data = {
            "file": SimpleUploadedFile("test.csv", b"col1,col2\n1,2"),
            "email": "void4function@gmail.com",
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CSVFile.objects.filter(id=response.data["id"]).exists())
