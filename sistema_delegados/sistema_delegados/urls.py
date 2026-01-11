from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

admin.site.site_header = "Panel de Control - Delegados"
admin.site.site_title = "Admin Delegados"
admin.site.index_title = "Bienvenido al Sistema de Gestión"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('elecciones.urls')),
]
