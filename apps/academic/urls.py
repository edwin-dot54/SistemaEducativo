from django.urls import path
from . import views

urlpatterns = [
    # ================= GRADOS =================
    path('grado/', views.grado_list, name='grado_list'),
    path('grado/<int:pk>/', views.grado_detail, name='grado_detail'),
    path('grado/create/', views.grado_create, name='grado_create'),
    path('grado/<int:pk>/edit/', views.grado_edit, name='grado_edit'),
    path('grado/<int:pk>/delete/', views.grado_delete, name='grado_delete'),
    
    # ================= MATERIAS =================
    path('materia/', views.materia_list, name='materia_list'),
    path('materia/<int:pk>/', views.materia_detail, name='materia_detail'),
    path('materia/create/', views.materia_create, name='materia_create'),
    path('materia/<int:pk>/edit/', views.materia_edit, name='materia_edit'),
    path('materia/<int:pk>/delete/', views.materia_delete, name='materia_delete'),
]