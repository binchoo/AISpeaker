from django.shortcuts import render
from . import getweather

# Create your views here.

def weather(request):
    question = request.GET['question']
    w = getweather.Weather()
    w.get_weather_page(question)
    loc = w.loc_data
    weatherdata = w.weather_data

    return render(request, 'weather.html',{'loc': loc, 'weatherdata': weatherdata, })