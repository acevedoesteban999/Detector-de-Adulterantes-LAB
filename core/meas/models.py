from django.db import models
from core.tra.models import Training
from config.utils import PredictionChoices
# Create your models here.
class Measuring(models.Model):
    name=models.CharField(verbose_name="Nombre",unique=True,max_length=15)
    datetime=models.DateTimeField(auto_now_add=True)
    training=models.ForeignKey(Training,null=True,related_name="measuring_trainig", on_delete=models.CASCADE)
    predict=models.CharField(max_length=1,choices=PredictionChoices,default="N")
    def __str__(self):
        return  self.name
    @staticmethod
    def chanels():
        return ["A","B","C","D","E","F","G","H","I","J","K","L","R","S","T","U","V","W"]
    def lamdas():
        return [410,435,460,485,510,535,560,585,601,645,680,705,730,760,810,860,900,940]
class MeasuringData(models.Model):
    chanel=models.CharField(verbose_name="Canal",max_length=1)
    value=models.FloatField(verbose_name="Valor",default=0)
    measuring=models.ForeignKey(Measuring, related_name="measuring_data",on_delete=models.CASCADE)
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
        