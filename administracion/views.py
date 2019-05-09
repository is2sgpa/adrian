# administracion/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http.response import HttpResponseRedirect

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class Login(FormView):
        # Establecemos la plantilla a utilizar
        template_name = 'registration/login.html'
        form_class = AuthenticationForm
        success_url = reverse_lazy("home.html")

        def dispatch(self, request, *args, **kwargs):
            # Si el usuario está autenticado entonces nos direcciona a la url establecida en success_url
            if request.user.is_authenticated():
                return HttpResponseRedirect(self.get_success_url())
            # Sino lo está entonces nos muestra la plantilla del login simplemente
            else:
                return super(Login, self).dispatch(request, *args, **kwargs)


        def form_valid(self, form):
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)
