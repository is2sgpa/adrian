# definicion/views.py
from definicion.models import Proyecto
from django.urls import reverse_lazy
from django.views import generic
from .forms import ProyectoCreationForm
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

@method_decorator(login_required, name='dispatch')
class CrearProyecto(generic.CreateView):

    form_class = ProyectoCreationForm
    success_url = reverse_lazy('proyectos')
    template_name = 'definicion/crear_proyecto.html'


    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(CrearProyecto, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class Proyectos(TemplateView):

    model = Proyecto
    template_name = 'definicion/proyectos.html'
    context_object_name = 'proyectos'
