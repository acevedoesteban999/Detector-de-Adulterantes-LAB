from django.db import models

# Create your models here.

IDENTF = [
    ("I", "Información"),
    ("R", "Reportes"),
    ("A", "Advertencias"),
    ("E", "Error"),
]
class BinnacleMessages(models.Model):
    identifier=models.CharField(max_length=1,choices=IDENTF)
    identifier_message=models.CharField(max_length=50)
    reason=models.CharField(max_length=50)
    timedate=models.DateTimeField(auto_now_add=True)