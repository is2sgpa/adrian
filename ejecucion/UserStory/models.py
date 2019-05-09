from django.db import models

# Create your models here.


class UserStory(models.Model):
    """DJANGO COLOCA AUTOMATICAMENTE UN CAMPO ID AUTOINCREMENTABLE como primary key=true, por lo tanto no es necesario poner codigo"""
    #Codigo: models.IntegerField()
    Nombre: models.CharField(max_length=25)
    #TipoUS: TipoUs
    ValorTecnico: models.IntegerField()
    ValorNegocio: models.IntegerField()
    Prioridad: models.FloatField()
    DescripcionBreve: models.CharField(max_length=50)
    Descripcion: models.CharField(max_length=100)
    """El tiempo estimado debe estar en horas"""
    TiempoEstimadoUS: models.IntegerField()
    #Sprint:Sprint
    #CriterioAceptacion: models.FloatField()
    #UserAsignado:Usuario
    Notas:models.CharField(max_length=20)
    TrabajoEjecutado: models.IntegerField()
    TrabajoRestante: models.CharField()
    #ArchivosAdjuntos: (ACA DEBEMOS PONER LA MANERA DE ADJUNTAR ARCHIVOS)
    """Aun faltan muchos atributos por agregar. VER LUEGO!!!"""


