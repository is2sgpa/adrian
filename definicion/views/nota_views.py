# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.urls import reverse, reverse_lazy
from django.forms.models import modelform_factory, inlineformset_factory, modelformset_factory
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic
from guardian.mixins import LoginRequiredMixin
from guardian.shortcuts import get_perms, get_perms_for_model, assign_perm
import reversion
from definicion.models import UserStory, Proyecto, MiembroEquipo, Sprint, Fase, Nota
from definicion.views import CreateViewPermissionRequiredMixin, GlobalPermissionRequiredMixin


class NotaDetail(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DetailView):
    """
    Vista de Detalles de una nota
    """
    model = Nota
    permission_required = 'project.view_project'
    template_name = 'project/nota/nota_detail.html'
    context_object_name = 'nota'

    def get_permission_object(self):
        '''
        Retorna el objeto al cual corresponde el permiso
        '''
        return self.get_object().user_story.proyecto

class NotaList(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.ListView):
    """
    Vista que devuelve una lista de notas del User Story deseado.
    """
    context_object_name = 'notas'
    template_name = 'project/nota/nota_list.html'
    permission_required = 'project.view_project'
    us = None

    def get_permission_object(self):
        '''
        Obtiene el user story
        '''
        us_pk = self.kwargs['pk']
        self.us = get_object_or_404(UserStory, pk=us_pk)
        return self.us.proyecto

    def get_queryset(self):
        """
        Obtiene el user story y sus versiones
        """
        return self.us.nota_set.all()

    def get_context_data(self, **kwargs):
        """
        Agrega el user story al contexto.
        """
        context = super(NotaList, self).get_context_data(**kwargs)
        context['userstory'] = self.us
        return context