from django.db import models


class CSVFile(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("error", "Error"),
    ]

    file = models.FileField(upload_to="csv_uploads/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    result = models.TextField(blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk} - {self.file.name}"
