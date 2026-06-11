from django.urls import path
from . import views

urlpatterns = [
    path('', views.pago_list, name='pago_list'),
    path('<int:pk>/', views.pago_detail, name='pago_detail'),
    path('create/', views.pago_create, name='pago_create'),
    path('<int:pk>/edit/', views.pago_edit, name='pago_edit'),
    path('<int:pk>/delete/', views.pago_delete, name='pago_delete'),
    path('<int:pk>/registrar/', views.pago_registrar, name='pago_registrar'),
]