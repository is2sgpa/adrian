# administracion/forms.py
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'nombre', 'apellido', 'direccion', 'telefono']

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nombre', 'apellido', 'direccion', 'telefono']

class UsuarioAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'nombre', 'apellido', 'direccion', 'telefono']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Other info', {'fields': ('nombre', 'apellido', 'direccion', 'telefono')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active',)}),
    )
