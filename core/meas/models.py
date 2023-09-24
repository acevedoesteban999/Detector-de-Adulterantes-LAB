from django.db import models
from core.tra.models import Training

# Create your models here.
class Measuring(models.Model):
    name=models.CharField(verbose_name="Nombre",unique=True,max_length=15)
    datetime=models.DateTimeField(auto_now_add=True)
    #prediction=models.FloatField(default=None,null=True)
    training=models.ForeignKey(Training,null=True, on_delete=models.CASCADE)
    def __str__(self):
        return  self.name

class Prediction(models.Model):
    measuring=models.OneToOneField(Measuring, on_delete=models.CASCADE)
    prediction=models.CharField(max_length=1)
    def __str__(self):
        return  self.pk    

class MeasuringData(models.Model):
    chanel=models.CharField(verbose_name="Canal",max_length=1)
    value=models.FloatField(verbose_name="Valor",default=0)
    measuring=models.ForeignKey(Measuring, on_delete=models.CASCADE)
    def __str__(self):
        return  f"{self.measuring}~{self.chanel}"
    def lamda(self):
        if  self.chanel=='A':
            return 410
        elif self.chanel=='B':
            return 435
        elif self.chanel=='C':
            return 460
        elif self.chanel=='D':
            return 485
        elif self.chanel=='E':
            return 510
        elif self.chanel=='F':
            return 535
        elif self.chanel=='G':
            return 560
        elif self.chanel=='H':
            return 585
        elif self.chanel=='I':
            return 610
        elif self.chanel=='J':
            return 645
        elif self.chanel=='K':
            return 680
        elif self.chanel=='L':
            return 705
        elif self.chanel=='R':
            return 730
        elif self.chanel=='S':
            return 760
        elif self.chanel=='T':
            return 810
        elif self.chanel=='U':
            return 860
        elif self.chanel=='V':
            return 900
        elif self.chanel=='W':
            return 940
        