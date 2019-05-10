# -*- coding: utf-8 -*-
#from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.views import generic
from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin
from guardian.shortcuts import get_perms
from definicion.forms import FaseFormSet, FlujosCreateForm, CreateFromPlantillaForm
from definicion.models import Flujo, Proyecto, UserStory, Sprint
from definicion.views import CreateViewPermissionRequiredMixin, GlobalPermissionRequiredMixin, ActiveProjectRequiredMixin


class FlujoList(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.ListView):
    """
    Vista de Listado de Flujos en el sistema
    """
    model = Flujo
    template_name = 'project/flujo/flujo_list.html'
    permission_required = 'project.view_project'
    context_object_name = 'flujos'
    project = None

    def get_permission_object(self):
        if not self.project:
            self.project = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return self.project

    def get_context_data(self, **kwargs):
        context = super(FlujoList, self).get_context_data(**kwargs)
        context['proyecto_perms'] = get_perms(self.request.user, self.project)
        return context

    def get_queryset(self):
        if not self.project:
            self.project = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return Flujo.objects.filter(proyecto=self.project)


class FlujoDetail(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DetailView):
    """
    Vista de Detalles de un flujo
    """
    model = Flujo
    template_name = 'project/flujo/flujo_detail.html'
    permission_required = 'project.view_project'
    context_object_name = 'flujo'

    def get_permission_object(self):
        '''
        Objeto por el cual comprobar el permiso
        '''
        return self.get_object().proyecto

    def get_context_data(self, **kwargs):
        """
        Agregar lista de fases al contexto
        :param kwargs: diccionario de argumentos claves
        :return: contexto
        """
        context = super(FlujoDetail, self).get_context_data(**kwargs)
        context['fases'] = [[a, a.userstory_set.count()]for a in self.object.fase_set.all()]
        context['act_us'] = [a.userstory_set.order_by('-prioridad') for a in self.object.fase_set.all()]
        us = self.object.proyecto.userstory_set.filter(fase__flujo=self.object) #User Stories del Flujo
        time = us.aggregate(registrado=Sum('tiempo_registrado'), estimado=Sum('tiempo_estimado')) #Aggregate retorna None en vez de 0
        context.update(time)
        return context


class FlujoDetailSprint(FlujoDetail):
    sprint = None

    def get_context_data(self, **kwargs):
        """
        Agregar lista de fases al contexto
        :param kwargs: diccionario de argumentos claves
        :return: contexto
        """
        self.sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_pk'])
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        context['fases'] = [[a, a.userstory_set.filter(sprint=self.sprint).count()] for a in self.object.fase_set.all()]
        context['sprint'] = self.sprint
        context['act_us'] = [a.userstory_set.filter(sprint=self.sprint).order_by('-prioridad') for a in self.object.fase_set.all()]
        us = self.object.proyecto.userstory_set.filter(fase__flujo=self.object, sprint=self.sprint) #User Stories del Flujo
        time = us.aggregate(registrado=Sum('tiempo_registrado'), estimado=Sum('tiempo_estimado'))
        context.update(time)
        return context


class AddFlujo(ActiveProjectRequiredMixin, LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.CreateView):
    """
    View que agrega un flujo al sistema
    """
    model = Flujo
    template_name = 'project/flujo/flujo_form.html'
    form_class = FlujosCreateForm
    permission_required = 'project.create_flujo'

    def get_proyecto(self):
        if not self.proyecto:
            self.proyecto = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return self.proyecto

    def get_permission_object(self):
        '''
        Objeto por el cual comprobar el permiso
        '''
        return get_object_or_404(Proyecto, id=self.kwargs['project_pk'])

    def get_context_data(self, **kwargs):
        """
        Agregar datos al contexto
        :param kwargs: argumentos clave
        :return: contexto
        """
        context = super(AddFlujo, self).get_context_data(**kwargs)
        context['current_action'] = "Agregar"

        context['fase_form'] = FaseFormSet(self.request.POST if self.request.method == 'POST' else None)
        return context

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del flujo agregado.
        """
        return reverse('project:flujo_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        """
        Comprobar validez del formulario. Crea una instancia de flujo para asociar con la fase
        :param form: formulario recibido
        :param fase_form: formulario recibido de fase
        :return: URL de redireccion
        """
        self.object = form.save(commit=False)
        self.object.proyecto = self.get_proyecto()
        self.object.proyecto.estado = 'EP'
        self.object.proyecto.save()
        self.object.save()
        fase_form = FaseFormSet(self.request.POST, instance=self.object)
        if fase_form.is_valid():
            fase_form.save()
            order = [form.instance.id for form in fase_form.ordered_forms]
            self.object.set_fase_order(order)

            return HttpResponseRedirect(self.get_success_url())

        return render(self.request, self.get_template_names(), {'form': form,
                                                                     'fase_form': fase_form},
                           context_instance=RequestContext(self.request))


class UpdateFlujo(ActiveProjectRequiredMixin, LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.UpdateView):
    """
    View que agrega un flujo al sistema
    """
    model = Flujo
    template_name = 'project/flujo/flujo_form.html'
    form_class = FlujosCreateForm
    permission_required = 'project.edit_flujo'

    def get_proyecto(self):
        return self.get_object().proyecto

    def get_permission_object(self):
        return self.get_object().proyecto

    def get_context_data(self, **kwargs):
        """
        Agregar datos al contexto
        :param kwargs: argumentos clave
        :return: contexto
        """
        context = super(UpdateFlujo, self).get_context_data(**kwargs)
        context['current_action'] = "Editar"
        context['fase_form'] = FaseFormSet(self.request.POST if self.request.method == 'POST' else None, instance=self.object)

        return context

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del flujo agregado.
        """
        return reverse('project:flujo_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        """
        Comprobar validez del formulario. Crea una instancia de flujo para asociar con la fase
        :param form: formulario recibido
        :param fase_form: formulario recibido de fase
        :return: URL de redireccion
        """
        self.object = form.save()
        fase_form = FaseFormSet(self.request.POST, instance=self.object)
        if fase_form.is_valid():
            fase_form.save()
            order = [form.instance.id for form in fase_form.ordered_forms]
            self.object.set_fase_order(order)

            return HttpResponseRedirect(self.get_success_url())

        return render(self.request, self.get_template_names(), {'form': form,
                                                                     'fase_form': fase_form},
                           context_instance=RequestContext(self.request))


class DeleteFlujo(ActiveProjectRequiredMixin, LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DeleteView):
    """
    Vista de Eliminacion de Flujos
    """
    model = Flujo
    template_name = 'project/flujo/flujo_delete.html'
    permission_required = 'project.delete_flujo'
    context_object_name = 'flujo'

    def get_proyecto(self):
        return self.get_object().proyecto

    def get_permission_object(self):
        return self.get_object().proyecto

    def get_success_url(self):
        return reverse_lazy('project:flujo_list', kwargs={'project_pk': self.get_object().proyecto.id})

class CreateFromPlantilla(ActiveProjectRequiredMixin, LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.FormView):
    '''
    Vista de creación a partir de plantillas
    '''
    template_name = 'project/flujo/flujo_createcopy.html'
    form_class = CreateFromPlantillaForm
    permission_required = 'project.create_flujo'

    def get_proyecto(self):
        if not self.proyecto:
            self.proyecto = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return self.proyecto

    def get_permission_object(self):
        return self.get_proyecto()

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del flujo agregado.
        """
        return reverse('project:flujo_detail', kwargs={'pk': self.flujo.id})

    def form_valid(self, form):
        new_flujo = form.cleaned_data['plantilla']
        proyecto = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        acti_set = new_flujo.fase_set.all()
        new_flujo.pk = None
        new_flujo.proyecto = proyecto
        proyecto.estado = 'EP'
        proyecto.save()
        new_flujo.save()
        self.flujo = new_flujo
        for fase in acti_set:
            fase.pk = None
            fase.flujo = new_flujo
            fase.save()

        return HttpResponseRedirect(self.get_success_url())
