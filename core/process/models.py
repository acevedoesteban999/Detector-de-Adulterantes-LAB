from django.db import models


# Create your models here.
class Measuring(models.Model):
    name=models.CharField(unique=True,max_length=15)
    #date=models.DateField(auto_now_add=True)
    #time=models.TimeField(auto_now_add=True)
    datetime=models.DateTimeField(auto_now_add=True)
    prediction=models.FloatField(default=None,null=True)
    def __str__(self):
        return  self.name
class MeasuringData(models.Model):
    chanel=models.CharField(max_length=1)
    value=models.FloatField(default=0)
    measuring=models.ForeignKey(Measuring, on_delete=models.CASCADE)
    def __str__(self):
        return  f"{self.measuring}~{self.chanel}"