# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy, reverse
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import DetailView
from django.views.generic import ListView
from guardian.mixins import LoginRequiredMixin
from definicion.forms import CustomUserChangeForm
from definicion.forms import CustomUserCreationForm
from definicion.views import GlobalPermissionRequiredMixin
from definicion.views import CreateViewPermissionRequiredMixin


class UserList(LoginRequiredMixin, ListView):
    """
    Lista de usuarios.
    """
    model = User
    context_object_name = 'users'
    template_name = 'project/user/user_list.html'

    def get_queryset(self):
        """
        Retorna una los usuarios excluyendo el AnonymousUser

        :return: lista de usuarios
        """
        return User.objects.exclude(id=-1)


class UserDetail(LoginRequiredMixin, DetailView):
    """
    Ver detalles de Usuario
    """
    model = User
    context_object_name = 'usuario'
    template_name = 'project/user/user_detail.html'

    def get_context_data(self, **kwargs):
        """
        Agregar lista de proyectos al contexto

        :param kwargs: diccionario de argumentos claves
        :return: contexto
        """
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['projects'] = self.object.miembroequipo_set.all()
        context['user_stories'] = self.object.userstory_set.order_by('-prioridad')
        return context


class AddUser(LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.CreateView):
    """
    Agregar un Usuario al Sistema
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = 'project/user/user_form.html'
    permission_required = 'auth.add_user'

    def get_context_data(self, **kwargs):
        context = super(AddUser, self).get_context_data(**kwargs)
        context['current_action'] = 'Agregar'
        return context

    def get_success_url(self):
        """
        Retorna una los usuarios excluyendo el AnonymousUser

        :return: url del UserDetail
        """
        return reverse('project:user_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        """
        Verificar validez del formulario

        :param form: formulario completado
        :return: Url de Evento Correcto
        """
        super(AddUser, self).form_valid(form)

        escogidas = self.request.POST.getlist('general_perms')
        for permname in escogidas:
            perm = Permission.objects.get(codename=permname)
            self.object.user_permissions.add(perm)

        return HttpResponseRedirect(self.get_success_url())


class DeleteUser(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DeleteView):
    """
    Eliminar un Usuario del Sistema
    """
    model = User
    template_name = 'project/user/user_delete.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('project:user_list')
    permission_required = 'auth.delete_user'

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class UpdateUser(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.UpdateView):
    """
    Actualizar un Usuario del Sistema
    """
    model = User
    template_name = 'project/user/user_form.html'
    permission_required = 'auth.change_user'
    form_class = modelform_factory(User, form=CustomUserChangeForm,
                                   fields=['first_name', 'last_name', 'email', 'username', 'is_active'], )

    def get_context_data(self, **kwargs):
        context = super(UpdateUser, self).get_context_data(**kwargs)
        context['current_action'] = 'Editar'
        return context

    def get_success_url(self):
        """
        Obtener url de evento correcto

        :return: url de UserDetail
        """
        return reverse('project:user_detail', kwargs={'pk': self.object.id})

    def get_initial(self):
        """
        Obtener datos iniciales para el formulario

        :return: diccionario con los datos iniciales
        """

        modelo = self.get_object()
        first_name= self.object.first_name
        last_name= self.object.last_name
        email=self.object.email
        username=self.object.username
        password=self.object.password
        perm_list = [perm.codename for perm in list(modelo.user_permissions.all())]

        initial = {'general_perms': perm_list , 'first_name':first_name, 'last_name':last_name, 'email':email, 'username':username, 'password':password}

        return initial

    def form_valid(self, form):
        """
        Comprobar validez del formulario recibido

        :param form: Formulario recibido
        :return: URL de evento correcto
        """
        super(UpdateUser, self).form_valid(form)
        # eliminamos permisos anteriores
        self.object.user_permissions.clear()
        escogidas = self.request.POST.getlist('general_perms')
        for permname in escogidas:
            perm = Permission.objects.get(codename=permname)
            self.object.user_permissions.add(perm)

        return HttpResponseRedirect(self.get_success_url())
