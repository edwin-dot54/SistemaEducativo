from django.urls import path
from . import views

urlpatterns = [
    path('tarea/', views.tarea_list, name='tarea_list'),
    path('tarea/<int:pk>/', views.tarea_detail, name='tarea_detail'),
    path('tarea/create/', views.tarea_create, name='tarea_create'),
    path('tarea/<int:pk>/edit/', views.tarea_edit, name='tarea_edit'),
    path('tarea/<int:pk>/delete/', views.tarea_delete, name='tarea_delete'),
]