from django.db import models
# Create your models here.

ActivationChoices=[
    ("r","relu"),
    ("t","tanh"),
    ("s","sigmoid"),
    ("l","linear"),
    ("m","softmax"),
]

class Model(models.Model):
    name=models.CharField(verbose_name="Nombre",unique=True,max_length=15)
    datetime=models.DateTimeField(auto_now_add=True)
    state=models.BooleanField(default=None,null=True)
    neurons=models.IntegerField(verbose_name="Neuronas",default=0)
    epochs=models.IntegerField(verbose_name="Épocas",default=0)
    activation=models.CharField(verbose_name="Activación",choices=ActivationChoices,default="r", max_length=1)
    def __str__(self):
        return  self.name