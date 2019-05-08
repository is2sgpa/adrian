from django.db import models
from django.conf import  settings
from django.contrib.auth import get_user_model

class Proyecto(models.Model):

    nombre=models.CharField(max_length=20, default='', null=False)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    miembros=models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
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