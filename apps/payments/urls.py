from django.urls import path
from . import views

urlpatterns = [
    path('pago/', views.pago_list, name='pago_list'),
    path('pago/<int:pk>/', views.pago_detail, name='pago_detail'),
    path('pago/create/', views.pago_create, name='pago_create'),
    path('pago/<int:pk>/edit/', views.pago_edit, name='pago_edit'),
    path('pago/<int:pk>/delete/', views.pago_delete, name='pago_delete'),
    path('pago/<int:pk>/registrar/', views.pago_registrar, name='pago_registrar'),
]