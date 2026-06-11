from django.urls import path
from . import views

urlpatterns = [
    # ================= ESTUDIANTE =================
    path('estudiante/', views.estudiante_list, name='estudiante_list'),
    path('estudiante/<int:pk>/', views.estudiante_detail, name='estudiante_detail'),
    path('estudiante/create/', views.estudiante_create, name='estudiante_create'),
    path('estudiante/<int:pk>/edit/', views.estudiante_edit, name='estudiante_edit'),
    path('estudiante/<int:pk>/delete/', views.estudiante_delete, name='estudiante_delete'),
    
    # ================= PROFESOR =================
    path('profesor/', views.profesor_list, name='profesor_list'),
    path('profesor/<int:pk>/', views.profesor_detail, name='profesor_detail'),
    path('profesor/create/', views.profesor_create, name='profesor_create'),
    path('profesor/<int:pk>/edit/', views.profesor_edit, name='profesor_edit'),
    path('profesor/<int:pk>/delete/', views.profesor_delete, name='profesor_delete'),
]