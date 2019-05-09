# administracion/urls.py
from django.conf.urls import url
from django.urls import path, re_path
from .views import SignUp, ListadoUsuarios, CrearUsuario, ModificarUsuario, DetalleUsuario

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    re_path(r'^usuarios/$', ListadoUsuarios.as_view(), name="listado_usuarios"),
    re_path(r'^crear_usuario/$', CrearUsuario.as_view(), name="crear_usuario"),
    re_path(r'^modificar_usuario/(?P<pk>\d+)/$', ModificarUsuario.as_view(), name="modificar_usuario"),
    re_path(r'^detalle_usuario/(?P<pk>\d+)/$',DetalleUsuario.as_view(), name="detalle_usuario"),

]