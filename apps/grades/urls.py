from django.urls import path
from . import views

urlpatterns = [
    path('', views.nota_list, name='nota_list'),
    path('<int:pk>/', views.nota_detail, name='nota_detail'),
    path('create/', views.nota_create, name='nota_create'),
    path('<int:pk>/edit/', views.nota_edit, name='nota_edit'),
    path('<int:pk>/delete/', views.nota_delete, name='nota_delete'),
]