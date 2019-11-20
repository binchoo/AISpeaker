from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home, name='news_home'),
    path('hls',views.headlines, name='headlines'),
    path('rks',views.rankings, name='rankings'),
    path('rankingRead.nhn',views.articleContent, name='articlecont'),
    path('voiceaudio',views.respondAudioFile, name='respondAudioFile'),
]