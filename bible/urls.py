from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.bible, name='bible'),
    path('today', views.todayBible, name='todayBible'),
    path('qa', views.qa, name='qa'),
]
