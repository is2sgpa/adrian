# administracion/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
#from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .forms import UsuarioAdmin
from .models import CustomUser

"""
class UsuarioAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ['username', 'email', 'nombre', 'apellido', 'direccion', 'telefono']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Other info', {'fields': ('nombre', 'apellido', 'direccion', 'telefono')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active',)}),
    )
"""
# Re-register UserAdmin
admin.site.register(CustomUser, UsuarioAdmin)