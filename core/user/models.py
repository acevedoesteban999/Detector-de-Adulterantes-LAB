from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    image=models.ImageField(upload_to='users',verbose_name="Imagen",default=None,null=True, height_field=None, width_field=None, max_length=None)
