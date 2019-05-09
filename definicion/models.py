from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from administracion.models import CustomUser

class Proyecto(models.Model):

    nombre=models.CharField(max_length=20, default='', null=False)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    descripcion_breve=models.CharField(max_length=100)
    descripcion_detallada=models.TextField(max_length=500)

    TIPOS_ESTADOS = (
        ('to_do', 'En Planificacion'),
        ('doing', 'En Ejecucion'),
        ('done', 'Hecho'),
    )

    estado=models.CharField(max_length=5, choices=TIPOS_ESTADOS, default='to_do')
    def get_nombre(self):
        return self.nombre

    def __str__(self):
        return self.get_nombre()

class Miembro():
    proyecto=models.ForeignKey(Proyecto, null=False, on_delete=models.CASCADE)
    usuario=models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)

    def _str_(self):
        return self.usuario.username