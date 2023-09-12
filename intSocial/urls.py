from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('usuario/', views.usuario),
    path('crear_usuario/', views.crear_usuario)
]
