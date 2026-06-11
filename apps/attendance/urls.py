from django.urls import path
from . import views

urlpatterns = [
    path('asistencia/', views.asistencia_list, name='asistencia_list'),
    path('asistencia/<int:pk>/', views.asistencia_detail, name='asistencia_detail'),
    path('asistencia/create/', views.asistencia_create, name='asistencia_create'),
    path('asistencia/<int:pk>/edit/', views.asistencia_edit, name='asistencia_edit'),
    path('asistencia/<int:pk>/delete/', views.asistencia_delete, name='asistencia_delete'),
]