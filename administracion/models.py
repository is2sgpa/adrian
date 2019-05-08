from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    nombre=models.CharField(max_length=20, default='', null=False)
    apellido = models.CharField(max_length=20, null=True)
    direccion=models.CharField(max_length=50, null=True)
    telefono=models.IntegerField(default=0000)

    def get_nombre(self):
        return self.nombre

    def __str__(self):
        return self.get_nombre()