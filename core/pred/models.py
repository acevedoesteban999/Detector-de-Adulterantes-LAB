from django.db import models
from core.meas.models import Measuring
from config.utils import PredictionChoices 
# Create your models here.


class Prediction(models.Model):
    name=models.CharField(verbose_name="Nombre",unique=True,max_length=15)
    state=models.BooleanField(default=None,null=True)
    datetime=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  self.name

class PredictionData(models.Model):
    predict=models.CharField(max_length=1,choices=PredictionChoices,default="P")
    prediction=models.ForeignKey(Prediction, on_delete=models.CASCADE)
    measuring=models.ForeignKey(Measuring, related_name="meas_prediction_data",on_delete=models.DO_NOTHING)
