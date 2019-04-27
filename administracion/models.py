from django.db import models
import uuid # Requerida para las instacias de usuarios unicos

# Create your models here.
class Usuario(models.Model):
    usuario= models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="ID único para el usuario")
    nombre=models.CharField(max_length=100)
    apellido=models.CharField(max_length=100)
    ci=models.BigIntegerField(help_text="Cedula de identidad")
    direccion=models.CharField(max_length=100)
    telefono=models.BigIntegerField()
    contraseña=models.CharField(max_length=70)
    email = models.CharField(max_length=50)

