#Personalización de la interfaz de admin en relación al modelo Usuario

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'cedula', 'first_name', 'last_name', 'seccion_base', 'is_staff') # Campos que se muestran en la lista de usuarios
    list_filter = ('seccion_base__carrera', 'is_staff') # Campos que se muestran en el filtro
    search_fields = ('cedula', 'first_name', 'last_name') # Campos que se muestran en la barra de búsqueda

    #Modificar campos de edición del usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Académica', {'fields': ('cedula', 'seccion_base')}),
    )
