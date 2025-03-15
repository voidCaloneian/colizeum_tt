# from django.contrib import admin
from django.urls import path
from csv_handler.views import CSVFileUploadView, CSVFileDetailView

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("api/upload/", CSVFileUploadView.as_view(), name="csv-upload"),
    path("api/file/<int:pk>/", CSVFileDetailView.as_view(), name="csv-detail"),
]
