from django.urls import path
from . import views

urlpatterns = [
    path('', views.asistencia_list, name='asistencia_list'),
    path('<int:pk>/', views.asistencia_detail, name='asistencia_detail'),
    path('create/', views.asistencia_create, name='asistencia_create'),
    path('<int:pk>/edit/', views.asistencia_edit, name='asistencia_edit'),
    path('<int:pk>/delete/', views.asistencia_delete, name='asistencia_delete'),
    path('fecha/<str:fecha>/', views.asistencia_fecha, name='asistencia_fecha'),
]