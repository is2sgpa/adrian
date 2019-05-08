# definicion/views.py
from definicion.models import Proyecto
from django.urls import reverse_lazy
from django.views import generic
from .forms import ProyectoCreationForm
from django.shortcuts import render
from django.contrib.auth import  decorators

class CrearProyecto(generic.CreateView):
    form_class = ProyectoCreationForm
    success_url = reverse_lazy('proyectos')
    template_name = 'definicion/crear_proyecto.html'

class Proyectos(generic.ListView):
    model = Proyecto
    template_name = 'definicion/proyectos.html'
    context_object_name = 'proyectos'