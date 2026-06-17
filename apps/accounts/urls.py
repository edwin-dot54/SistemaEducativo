from django.urls import path
from . import views

urlpatterns = [
    # ================= AUTENTICACIÓN =================
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registro/', views.registro_view, name='registro'),
    
    # ================= USUARIOS =================

    path('usuario/', views.usuario_list, name='usuario_list'),
    path('usuario/<int:pk>/', views.usuario_detail, name='usuario_detail'),
    path('usuario/create/', views.usuario_create, name='usuario_create'),
    path('usuario/<int:pk>/edit/', views.usuario_edit, name='usuario_edit'),
    path('usuario/<int:pk>/delete/', views.usuario_delete, name='usuario_delete'),
    
    # ================= ROLES =================
    path('rol/', views.rol_list, name='rol_list'),
    path('rol/create/', views.rol_create, name='rol_create'),
    path('rol/<int:pk>/edit/', views.rol_edit, name='rol_edit'),
    path('rol/<int:pk>/delete/', views.rol_delete, name='rol_delete'),
]