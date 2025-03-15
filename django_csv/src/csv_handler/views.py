from typing import Any
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CSVFile
from .serializers import CSVFileUploadSerializer
from .tasks import process_csv_file


class CSVFileUploadView(APIView):
    """
    Загрузка CSV файла
    """

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Загрузка CSV файла
        """
        serializer = CSVFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            csv_instance: CSVFile = serializer.save(status="new")
            # Инициируем асинхронную задачу обработки CSV
            process_csv_file.delay(csv_instance.id)
            return Response(
                {"id": csv_instance.id, "status": csv_instance.status},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CSVFileDetailView(generics.RetrieveAPIView):
    queryset = CSVFile.objects.all()
    serializer_class = CSVFileUploadSerializer
