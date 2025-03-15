from rest_framework import serializers
from .models import CSVFile


class CSVFileUploadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для загрузки CSV файла
    """

    class Meta:
        model = CSVFile
        fields = ("id", "email", "status")
