from django.db import models
# Create your models here.

class Model(models.Model):
    name=models.CharField(verbose_name="Nombre",unique=True,max_length=15)
    datetime=models.DateTimeField(auto_now_add=True)
    state=models.BooleanField(default=None,null=True)
    #accuracy=models.FloatField(default=0)
    #loss=models.FloatField(default=0)
    #file_model=models.FileField(upload_to="models")
    def __str__(self):
        return  self.name