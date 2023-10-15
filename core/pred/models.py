from django.db import models
from core.meas.models import Measuring
# Create your models here.


class Prediction(Measuring):
    state=models.BooleanField(default=None,null=True)
    def __str__(self):
        return  self.name

