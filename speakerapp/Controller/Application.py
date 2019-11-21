import requests


class Application:

    def __init__(self):
        self.app_url = 'http://127.0.0.1:8000/'

    def execute(self, question):
        response = requests.get(self.app_url, {'question': question})
        return response


class StockApplication(Application):

    def __init__(self):
        self.app_url = 'http://127.0.0.1:8000/chart'


class WeatherApplication(Application):

    def __init__(self):
        self.app_url = 'http://127.0.0.1:8000/weather'


class NewsApplication(Application):

    def __init__(self):
        self.app_url = 'http://127.0.0.1:8000/news'


class BibleApplication(Application):

    def __init__(self):
        self.app_url = 'http://127.0.0.1:8000/bible'
