from django.contrib import admin
from django.urls import path
from . import views
from bible import views as bible_views

urlpatterns = [
    path('home',views.home, name='news_home'),
    path('hls',views.headlines, name='headlines'),
    path('rks',views.rankings, name='rankings'),
    path('voiceaudio',views.respondAudioFile, name='respondAudioFile'),
    path('qa', bible_views.qa, name='news_qa')
]