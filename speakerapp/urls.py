from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #speaker/
    path('', views.speaker, name='speaker'),

    #speaker/result
    path('result', views.result, name='result'),

    #speaker/wait
    path('wait', views.wait, name = 'wait'),

    #speaker/controller
    path('controller', views.controller, name='controller'),
]