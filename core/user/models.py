from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    image=models.ImageField(upload_to='users',verbose_name="Imagen",default='no_user_imagen.jpg',null=True, height_field=None, width_field=None, max_length=None)
    class Meta:
        permissions = (
            ("is_development", "is_development"),
            ("is_admin", "is_admin"),
            ("is_guest ", "is_guest"),
            ("act_desact_user","act_desact_user"),
            ("view_binnacle","view_binnacle"),
            ("view_performance","view_performance"),
            )