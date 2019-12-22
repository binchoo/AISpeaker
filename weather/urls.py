from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #speaker/weather
    path('', views.weather, name='weather'),
    path('temperature', views.temperature, name='temperature'),
    path('rain', views.rain, name='rain'),
    path('ozon', views.ozon, name='ozon'),
    path('finedust', views.finedust, name='finedust'),

]