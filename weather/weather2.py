# coding:utf-8
import datetime
import pytz
import urllib.request
import json
import time


class Weather:
      def __init__(self):#, mirror_list):
            self.data = {}
            #self.mirror_list = mirror_list
            # 
      def get_api_date(self):
            date_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
            check_date = int(date_now)
            return (str(check_date), "0200")

      @property
      def get_weather_data(self):
            api_date, api_time = self.get_api_date()
            url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
            key = "serviceKey=" + '6h85ymiuerjoMWrN4hcNYKw9WKoakFovGEvoZgvspK11p37pFe1mAF1cFftuaPkM2wBrDBxvMuFj7a%2B%2BSNrPSw%3D%3D'
            date = "&base_date=" + api_date
            time = "&base_time=" + api_time
            nx = "&nx=59"
            ny = "&ny=125"
            numOfRows = "&numOfRows=100"
            type = "&_type=json"
            api_url = url + key + date + time + nx + ny + numOfRows + type

            data = urllib.request.urlopen(api_url).read().decode('utf8')
            data_json = json.loads(data)
            parsed_json = data_json['response']['body']['items']['item']

            passing_data = {}

            dt = datetime.datetime.now()

            for one_parsed in parsed_json:
                  if one_parsed['fcstDate'] == int(api_date) and one_parsed['category'] in ['TMX', 'TMN']:
                        passing_data[one_parsed['category']] = one_parsed['fcstValue']
                  elif int(dt.hour) * 100 + int(dt.minute) >= int(one_parsed['fcstTime']) - 150:
                        if int(dt.hour) * 100 + int(dt.minute) <= int(one_parsed['fcstTime']) + 150:
                              passing_data[one_parsed['category']] = one_parsed['fcstValue']
            return passing_data

      def get_max_tem(self): # 최� 기온
            data = self.get_weather_data
            tmx = data['TMX']
            return tmx

      def get_min_tem(self): # 최� �기온
            data = self.get_weather_data
            tmn = data['TMN']

            return tmn

      def get_cur_tem(self): # 현재기온
            data = self.get_weather_data
            t3h = data['T3H']

            return t3h

      def get_is_rain(self): # 비오는지
            '''
            0 : 없음
            1 : 비
            2 : 비/눈
            3 : 눈
            '''
            data = self.get_weather_data
            pty = data['PTY']

            return pty

      def get_is_cloudy(self): # 흐린지
            '''
               1 : 맑음
               2 : 구름조금
               3 : 구름많음
               4 : 흐림
               '''
            data = self.get_weather_data
            sky = data['SKY']

            return sky

      def get_cur_sky(self):

            cur_sky = ''

            rain = self.get_is_rain()
            cloud = self.get_is_cloudy()

            if rain == 0:
                  if cloud == 1:
                        cur_sky = '맑음'
                  elif cloud == 2:
                        cur_sky = '흐림'
                  elif cloud == 3:
                        cur_sky = '매우흐림'
                  elif cloud == 4:
                        cur_sky = '안개낌'
            elif rain == 1:
                  cur_sky = '비 내림'
            elif rain == 2:
                  cur_sky = '눈과 비 내림'
            elif rain == 3:
                  cur_sky = '눈 내림'

            return cur_sky

      def get_json_data(self):
            cur_weather_json = {
                  'cur_tem': self.get_cur_tem(),
                  'min_tem': self.get_min_tem(),
                  'max_tem': self.get_max_tem(),
                  'cur_sky': self.get_cur_sky()
            }
            return cur_weather_json

if __name__ == "__main__":
      w = Weather()
      print(w.get_max_tem())
      print(w.get_json_data())
      print(w.get_cur_sky())