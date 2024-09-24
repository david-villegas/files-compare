from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('comparar', views.comparar_archivos, name='comparar'),
]
