# definicion/urls.py
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('crear_proyecto/', views.CrearProyecto.as_view(), name='crear_proyecto'),
    path('proyectos/', views.Proyectos.as_view(), name='proyectos'),
]