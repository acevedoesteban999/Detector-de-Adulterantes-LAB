from django.db import models


# Create your models here.
class Measuring(models.Model):
    name=models.CharField(max_length=15)
    chanel=models.CharField(max_length=1)
    value=models.FloatField(default=0)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    prediction=models.FloatField(default=0)
