from django.db import models
from core.mod.models import Model
# Create your models here.


    
class Training(models.Model):
    name=models.CharField(verbose_name="Nombre",unique=True,max_length=15)
    datetime=models.DateTimeField(auto_now_add=True)
    count=models.IntegerField(verbose_name="Cantidad")
    models=models.ManyToManyField(Model)
    def __str__(self):
        return  self.name