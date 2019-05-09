# administracion/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import CustomUser

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class Login(FormView):
        # Establecemos la plantilla a utilizar
        template_name = 'registration/login.html'
        form_class = AuthenticationForm
        success_url = reverse_lazy('home')

        def form_valid(self, form):
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)

"""
        def dispatch(self, request, *args, **kwargs):
            # Si el usuario está autenticado entonces nos direcciona a la url establecida en success_url
            if request.user.is_authenticated():
                return HttpResponseRedirect(stemporal96elf.get_success_url())
            # Sino lo está entonces nos muestra la plantilla del login simplemente
            else:
                return super(Login, self).dispatch(request, *args, **kwargs)
"""


class Inicio(TemplateView):
    template_name = "home.html"

class ListadoUsuarios(ListView):
    model = CustomUser
    template_name = 'usuarios/usuarios.html'
    context_object_name = 'usuarios'

class CrearUsuario(CreateView):
    template_name = 'usuarios/usuario.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('listado_usuarios')

class ModificarUsuario(UpdateView):
    model = CustomUser
    template_name = 'usuarios/modificar_usuario.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('listado_usuarios')

class DetalleUsuario(DetailView):
    model = CustomUser
    template_name = 'usuarios/detalle_usuario.html'