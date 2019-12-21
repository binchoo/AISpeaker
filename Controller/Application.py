import requests
'''
execute(self, question) 인터페이스를 준수하는 앱 모음
'''
class Application :
    sub_url = ''
    app_url = 'http://127.0.0.1:8000/'

    def __init__(self) :
        self.app_url += self.sub_url
    
    def execute(self, question) :
        response = requests.get(self.app_url, {'question' : question})
        return response

class WeatherApplication(Application) :
    app_url = 'http://127.0.0.1:8000/weather'

class TemperatureApplication(WeatherApplication) :
    sub_url = '/temperature'

class FineDustApplication(WeatherApplication) :
    sub_url = '/finedust'

class RainApplication(WeatherApplication) :
    sub_url = '/rain'
    
class OzonApplication(WeatherApplication) :
    sub_url = '/ozon'

class NewsApplication(Application) :

    app_url = 'http://127.0.0.1:8000/news/hls'

    def execute(self, question) :
        response = requests.get(self.app_url)
        return response

class StockApplication(Application) :
    app_url = 'http://127.0.0.1:8000/chart'

class BibleApplication(Application) :
    app_url = 'http://127.0.0.1:8000/bible'

class TodayBibleApplication(BibleApplication) :
    sub_url = '/today'

from django.http import HttpResponse
class NoneApplication(Application) :
    def execute(self, question) :
        return HttpResponse("Oops, I don't understand.")