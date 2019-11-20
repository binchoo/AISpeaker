"""AISpeaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
##다른 앱들 import
#import account.views
import speakerapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',speakerapp.views.home, name='home'),

    #/speaker/~
    path('speaker/', include('speakerapp.urls')), 

    #/account/~
    path('account/', include('account.urls')),

    #/controller/stock/~
    path('chart/', include('chart.urls')),

    #/controller/news/~
    path('news/', include('news.urls')),

    #/controller/bible/~
    path('bible/', include('bible.urls')),

    #/controller/weather/~
    path('weather/', include('weather.urls')),
]
