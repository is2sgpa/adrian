# definicion/forms.py

from django import forms
from .models import Proyecto

class ProyectoCreationForm(forms.ModelForm):

  class Meta:
        model = Proyecto
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'miembros', 'descripcion_breve', 'descripcion_detallada', 'estado']

class ProyectoChangeForm(forms.ModelForm):

    class Meta:
        model = Proyecto
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'miembros', 'descripcion_breve', 'descripcion_detallada', 'estado']