from django.db import models
from django.contrib.auth import get_user_model
"""
class UserStory(models.Model):
    nombre:models.CharField(max_length=20, blank=True, null=False)
    #tipoUS=
    valor_tecnico=models.IntegerField()
    valor_negocio=models.IntegerField()
    prioridad=models.DecimalField(max_digits=10, decimal_places=2)
    descripcion_breve=models.CharField(max_length=100, blank=True, null=False)
    tiempo_estimado=models.IntegerField(help_text="El valor ingresado serà en horas")
    #sprint=
    criterio_aceptacion=models.DecimalField(max_digits=10, decimal_places=2)
    usuario_asignado=models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
"""