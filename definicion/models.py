from django.db import models

from administracion.models import Usuario


# Create your models here.
class Proyecto(models.Model):

    ESTADOS_PROYECTO = (
        ('TO_DO','En planificacion'),
        ('DOING','En ejecucion'),
        ('DONE','Terminado'),
    )
    nombre=models.CharField(max_length=100)
    fecha_inicio=models.DateField('fecha_de_inicio')
    fecha_fin=models.DateField('fecha_de_finalizacion')
    miembros=models.ManyToManyField(Usuario)
    descripcion_breve=models.CharField(max_length=100)
    descripcion_detallada=models.TextField(max_length=1000)
    estado=models.CharField(max_length=5, choices=ESTADOS_PROYECTO, blank=True, default='Planificacion', help_text='Estado actual del Proyecto')

    def __str__(self):
        return self.nombre
