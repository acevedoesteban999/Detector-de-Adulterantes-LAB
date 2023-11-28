from django.db import models
from core.meas.models import Measuring
from config.utils import PredictionChoices 
# Create your models here.



class Prediction(models.Model):
    name=models.CharField(verbose_name="Nombre",unique=True,max_length=15)
    state=models.BooleanField(default=None,null=True)
    predict=models.CharField(max_length=1,choices=PredictionChoices,default="N")
    measuring=models.ForeignKey(Measuring,related_name="prediction_meas", on_delete=models.DO_NOTHING)
    datetime=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  self.name   

