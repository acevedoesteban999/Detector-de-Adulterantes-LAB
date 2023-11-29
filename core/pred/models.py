from django.db import models
from core.meas.models import Measuring
from config.utils import PredictionChoices 
from core.mod.models import Model
# Create your models here.


class Prediction(models.Model):
    name=models.CharField(verbose_name="Nombre",unique=True,max_length=15)
    state=models.BooleanField(default=None,null=True)
    datetime=models.DateTimeField(auto_now_add=True)
    model=models.ForeignKey(Model, on_delete=models.CASCADE)
    def __str__(self):
        return  self.name

class PredictionData(models.Model):
    predict=models.CharField(max_length=1,choices=PredictionChoices,default="P")
    prdict_value=models.FloatField(default=0)
    prediction=models.ForeignKey(Prediction, on_delete=models.CASCADE)
    measuring=models.ForeignKey(Measuring, related_name="meas_prediction_data",on_delete=models.DO_NOTHING)
