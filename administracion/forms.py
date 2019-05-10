# administracion/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser
from django.contrib.auth.models import Group, Permission, User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from guardian.shortcuts import get_perms_for_model
from definicion.models import Proyecto, Flujo, Sprint, UserStory
from django.forms.models import inlineformset_factory, BaseInlineFormSet
#from definicion.forms import __general_perms_list__
"""
def __user_and_group_permissions__():
    perms_user_list = [(perm.codename, perm.name) for perm in get_perms_for_model(CustomUser)]
    perms_group_list = [(perm.codename, perm.name) for perm in get_perms_for_model(Group)]
    perms = []
    perms.extend(perms_user_list)
    perms.extend(perms_group_list)
    return perms
"""

class CustomUserCreationForm(UserCreationForm):
    """
    general_perms_list = [(perm.codename, perm.name) for perm in __general_perms_list__()]
    general_perms_list.extend(__user_and_group_permissions__())
    general_perms = forms.MultipleChoiceField(general_perms_list, widget=forms.CheckboxSelectMultiple,
                                              label="General permissions", required=False)
    """
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'nombre', 'apellido', 'direccion', 'telefono']

class CustomUserChangeForm(UserChangeForm):
    """
    Formulario para edición de usuarios
    """
    """
    general_perms_list = [(perm.codename, perm.name) for perm in __general_perms_list__()]
    general_perms_list.extend(__user_and_group_permissions__())
    general_perms = forms.MultipleChoiceField(general_perms_list, widget=forms.CheckboxSelectMultiple, label="General permissions", required=False)
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nombre', 'apellido', 'direccion', 'telefono']

class RolForm(forms.ModelForm):
    '''
    Formulario para el manejo de roles
    '''

    """
    perms_proyecto_list = [(perm.codename, perm.name) for perm in get_perms_for_model(Proyecto) if 'proyecto' in perm.codename]
    perms_userstories_list = [(perm.codename, perm.name) for perm in get_perms_for_model(Proyecto) if 'userstory' in perm.codename]
    perms_userstories_list.extend([(perm.codename, perm.name) for perm in get_perms_for_model(UserStory)])
    perms_flujo_list = [(perm.codename, perm.name) for perm in get_perms_for_model(Proyecto) if 'flujo' in perm.codename and not('template' in perm.codename)]
    perms_sprint_list = [(perm.codename, perm.name) for perm in get_perms_for_model(Proyecto) if 'sprint' in perm.codename]

    #perms_list = [(perm.codename, perm.name) for perm in Permission.objects.all()] #alternativa con una sola lista

    perms_proyecto = forms.MultipleChoiceField(perms_proyecto_list, widget=forms.CheckboxSelectMultiple, label=Proyecto._meta.verbose_name_plural.title(), required=False)
    perms_userstory = forms.MultipleChoiceField(perms_userstories_list, widget=forms.CheckboxSelectMultiple, label=UserStory._meta.verbose_name_plural.title(), required=False)
    perms_flujo = forms.MultipleChoiceField(perms_flujo_list, widget=forms.CheckboxSelectMultiple, label=Flujo._meta.verbose_name_plural.title(), required=False)
    perms_sprint = forms.MultipleChoiceField(perms_sprint_list, widget=forms.CheckboxSelectMultiple, label=Sprint._meta.verbose_name_plural.title(), required=False)
    #perms = forms.MultipleChoiceField(perms_list, widget=forms.CheckboxSelectMultiple, label="Permisos", required=False)
    """
    class Meta:
        model = Group
        fields = ["name"]
