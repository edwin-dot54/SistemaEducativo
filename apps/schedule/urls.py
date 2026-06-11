from django.urls import path
from . import views

urlpatterns = [
    path('horario/', views.horario_list, name='horario_list'),
    path('horario/<int:pk>/', views.horario_detail, name='horario_detail'),
    path('horario/create/', views.horario_create, name='horario_create'),
    path('horario/<int:pk>/edit/', views.horario_edit, name='horario_edit'),
    path('horario/<int:pk>/delete/', views.horario_delete, name='horario_delete'),
    path('horario/grado/<int:pk>/', views.horario_por_grado, name='horario_por_grado'),
]