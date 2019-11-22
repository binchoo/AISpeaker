import requests
'''
execute(self, question) 인터페이스를 준수하는 앱 모음
'''


class Application:

    app_url = 'http://127.0.0.1:8000/'

    def execute(self, question):
        response = requests.get(self.app_url, {'question': question})
        return response


class StockApplication(Application):
    app_url = 'http://127.0.0.1:8000/chart'


class WeatherApplication(Application):
    app_url = 'http://127.0.0.1:8000/weather'


class NewsApplication(Application):

    app_url = 'http://127.0.0.1:8000/news/hls'

    def execute(self, question):
        response = requests.get(self.app_url)
        return response


class BibleApplication(Application):
    app_url = 'http://127.0.0.1:8000/bible'
