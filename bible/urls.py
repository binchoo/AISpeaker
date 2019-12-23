from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.bible, name='bible'),
    path('today', views.todayBible, name='todayBible'),
    path('qa', views.qa, name='qa'),
    path('qa2', views.qa2, name='qa2'),
    path('more', views.more, name='more'),
]
