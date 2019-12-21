from django.shortcuts import render
from . import getweather

# Create your views here.

def make_weahter_view(request, sub_type) :
    question = request.GET['question']
    w = getweather.Weather()
    loc = w.get_location(question)
    w.get_weather_page(sub_type, loc)
    weatherdata = w.weather_data
    return render(request, 'weather.html',{'loc': loc, 'weatherdata': weatherdata, })

def weather(request):
    return make_weahter_view(request, 'weather')

def temperature(request) :
    return make_weahter_view(request, 'temperature')

def rain(request) :
    return make_weahter_view(request, 'rain')

def ozon(request) :
    return make_weahter_view(request, 'ozon')

def finedust(request) :
    return make_weahter_view(request, 'finedust')