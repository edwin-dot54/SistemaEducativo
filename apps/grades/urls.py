from django.urls import path
from . import views

urlpatterns = [
    path('nota/', views.nota_list, name='nota_list'),
    path('nota/<int:pk>/', views.nota_detail, name='nota_detail'),
    path('nota/create/', views.nota_create, name='nota_create'),
    path('nota/<int:pk>/edit/', views.nota_edit, name='nota_edit'),
    path('nota/<int:pk>/delete/', views.nota_delete, name='nota_delete'),
]