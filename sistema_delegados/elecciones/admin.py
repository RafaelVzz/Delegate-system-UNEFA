from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib import messages
from .models import Materia, Eleccion, Voto

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_materia', 'codigo_materia', 'seccion', 'delegado_actual_link')
    list_filter = ('seccion__carrera', 'seccion')
    search_fields = ('nombre_materia', 'codigo_materia')
    actions = ['destituir_delegado']

    def delegado_actual_link(self, obj):
        if obj.delegado_actual:
            return obj.delegado_actual
        return mark_safe('<span style="color: red;">VACANTE</span>')
    delegado_actual_link.short_description = 'Delegado Actual'

    @admin.action(description='Destituir Delegado y reiniciar elecciones')
    def destituir_delegado(self, request, queryset):
        count = queryset.update(delegado_actual=None)
        self.message_user(request, f"Se han destituido {count} delegados. Las elecciones quedan abiertas de nuevo.", messages.SUCCESS)

@admin.register(Eleccion)
class EleccionAdmin(admin.ModelAdmin):
    list_display = ('materia', 'token_acceso', 'esta_activa', 'fecha_creacion')
    list_filter = ('esta_activa',)
    actions = ['cerrar_elecciones_masivo']

    @admin.action(description='Cerrar elecciones seleccionadas')
    def cerrar_elecciones_masivo(self, request, queryset):
        count = queryset.update(esta_activa=False)
        self.message_user(request, f"Se han cerrado {count} elecciones.", messages.SUCCESS)

# Register Voto mostly for debugging/completeness, though not explicitly requested customized
admin.site.register(Voto)
