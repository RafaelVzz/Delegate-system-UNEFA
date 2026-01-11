from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('materia/<int:materia_id>/', views.materia_detalle, name='materia_detalle'),
    path('eleccion/<int:eleccion_id>/votar/', views.votar_eleccion, name='votar_eleccion'),
    path('auto-asignar/', views.confirmar_auto_asignacion, name='confirmar_auto_asignacion'),
]
