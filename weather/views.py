from django.shortcuts import render
from . import getweather

# Create your views here.

def weather(request):
    question = request.GET['question']
    w = getweather.Weather()
    loc = w.get_location(question)
    w.get_weather_page('weather', loc)
    weatherdata = w.weather_data
    return render(request, 'weather.html',{'loc': loc, 'weatherdata': weatherdata, })

def temperature(request) :
    question = request.GET['question']
    w = getweather.Weather()
    loc = w.get_location(question)
    w.get_weather_page('temperature', loc)
    weatherdata = w.weather_data
    return render(request, 'weather.html',{'loc': loc, 'weatherdata': weatherdata, })

def rain(request) :
    question = request.GET['question']
    w = getweather.Weather()
    loc = w.get_location(question)
    w.get_weather_page('rain', loc)
    weatherdata = w.weather_data
    return render(request, 'weather.html',{'loc': loc, 'weatherdata': weatherdata, })

def ozon(request) :
    question = request.GET['question']
    w = getweather.Weather()
    loc = w.get_location(question)
    w.get_weather_page('ozon', loc)
    weatherdata = w.weather_data
    return render(request, 'weather.html',{'loc': loc, 'weatherdata': weatherdata, })

def finedust(request) :
    question = request.GET['question']
    w = getweather.Weather()
    loc = w.get_location(question)
    w.get_weather_page('finedust', loc)
    weatherdata = w.weather_data
    return render(request, 'weather.html',{'loc': loc, 'weatherdata': weatherdata, })