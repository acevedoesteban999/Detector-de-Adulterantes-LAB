from django.db import models
from core.mod.models import Model
from config.utils import PredictionChoices
# Create your models here.


    
class Training(models.Model):
    name=models.CharField(verbose_name="Nombre",unique=True,max_length=15)
    datetime=models.DateTimeField(auto_now_add=True)
    count=models.IntegerField(default=0,verbose_name="Cantidad")
    predict=models.CharField(max_length=1,choices=PredictionChoices,default="N")
    models=models.ManyToManyField(Model,related_name="training_model")
    
    def __str__(self):
        return  self.name