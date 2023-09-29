from django.db import models
from core.meas.models import Measuring
# Create your models here.


class Prediction(Measuring):
    def __str__(self):
        return  self.name

