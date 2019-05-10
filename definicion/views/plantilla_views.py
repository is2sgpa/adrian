# -*- coding: utf-8 -*-
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.views import generic
from guardian.mixins import LoginRequiredMixin
from definicion.forms import PlantillaCreateForm, FaseFormSet
from definicion.models import Flujo
from definicion.views import CreateViewPermissionRequiredMixin, GlobalPermissionRequiredMixin


class PlantillaList(LoginRequiredMixin, generic.ListView):
    """
    Vista de Listado de Plantillas en el sistema
    """
    model = Flujo
    template_name = 'project/plantilla/plantilla_list.html'
    context_object_name = 'plantillas'
    queryset = Flujo.objects.filter(proyecto_id=None)


class PlantillaDetail(LoginRequiredMixin, generic.DetailView):
    """
    Vista de Detalles de una Plantilla
    """
    model = Flujo
    template_name = 'project/plantilla/plantilla_detail.html'
    context_object_name = 'plantilla'


class AddPlantilla(LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.CreateView):
    """
    View que agrega un flujo al sistema
    """
    model = Flujo
    template_name = 'project/plantilla/plantilla_form.html'
    form_class = PlantillaCreateForm
    permission_required = 'project.add_flow_template'

    def get_context_data(self, **kwargs):
        """
        Agregar datos al contexto
        :param kwargs: argumentos clave
        :return: contexto
        """
        context = super(AddPlantilla, self).get_context_data(**kwargs)
        context['current_action'] = "Agregar"
        if (self.request.method == 'GET'):
            context['fase_form'] = FaseFormSet()
        return context

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del flujo agregado.
        """
        return reverse('project:plantilla_detail', kwargs={'pk': self.object.id})

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

        return self.render(self.request, self.get_template_names(), {'form': form,
                                                                     'fase_form': fase_form},
                           context_instance=RequestContext(self.request))


class UpdatePlantilla(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.UpdateView):
    """
    View que agrega un flujo al sistema
    """
    model = Flujo
    template_name = 'project/plantilla/plantilla_form.html'
    form_class = PlantillaCreateForm
    permission_required = 'project.change_flow_template'

    def get_context_data(self, **kwargs):
        """
        Agregar datos al contexto
        :param kwargs: argumentos clave
        :return: contexto
        """
        context = super(UpdatePlantilla, self).get_context_data(**kwargs)
        context['current_action'] = "Actualizar"
        if (self.request.method == 'GET'):
            context['fase_form'] = FaseFormSet(instance=self.object)

        return context

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del flujo agregado.
        """
        return reverse('project:plantilla_detail', kwargs={'pk': self.object.id})

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


class DeletePlantilla(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DeleteView):
    """
    Vista de Eliminacion de Plantillas
    """
    model = Flujo
    template_name = 'project/plantilla/plantilla_delete.html'
    context_object_name = 'plantilla'
    success_url = reverse_lazy('project:plantilla_list')
    permission_required = 'project.delete_flow_template'


