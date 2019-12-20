# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
# from pprint import pprint
import requests
import re


class Weather:
    def __init__(self):
        self.weather_data = ""
        self.loc_data = ""

    def get_location(self, voice):
        regex = re.compile("서울|인천|대전|대구|울산|부산|광주|제주|세종|전주|화양동")
        search_str = regex.search(voice)
        if search_str != None:
            # print('위치: ' + search_str.group(0))
            self.loc_data = '위치: ' + search_str.group(0) + ' 날씨'
            return search_str.group(0)
        else:
            # print('위치: 광진구')
            self.loc_data = '위치: 광진구 날씨'
            return '광진구'

    def get_weather_page(self, q_type, loc):
     
        # 네이버 날씨 페이지 가져오기
        html = requests.get('https://search.naver.com/search.naver?query=' + loc + '날씨')
        
        # pprint(html.text)
        soup = bs(html.text, 'html.parser')  # 파싱
        if q_type == 'weather':
            self.print_all_weather(soup)
        elif q_type == 'temperature':
            self.get_today_tem(soup)
        elif q_type == 'finedust' or q_type == 'ozon':
            self.get_weather_dust(soup)
        elif q_type == 'rain':
            is_rain = self.get_weather_detail(soup)
            if is_rain == 1:
                # print("비소식이있습니다. 우산을 챙기세요.")
                self.weather_data += "비소식이있습니다. 우산을 챙기세요. "
            elif is_rain == 2:
                # print("눈소식이 있습니다. 우산을 챙기세요.")
                self.weather_data += "눈소식이 있습니다. 우산을 챙기세요. "
            else:
                # print("비나 눈소식이 없습니다.")
                self.weather_data += "비나 눈소식이 없습니다. "

    def get_today_tem(self, soup):
        # 오늘온도
        today_tem = soup.find('span', {'class': 'todaytemp'}).text
        # print('현재온도 ' + today_tem + '˚에요')
        self.weather_data += '현재온도 ' + today_tem + '˚에요. '
        # 최소온도
        info_list = soup.find('ul', {'class': 'info_list'})
        info_list_li = info_list.findAll('li')
        min_tem = info_list_li[1].find('span', {'class': 'min'}).text
        # print('최소온도 ' + min_tem + '에요')
        self.weather_data += '최소온도 ' + str(min_tem) + '에요. '

        # 최고온도
        max_tem = info_list_li[1].find('span', {'class': 'max'}).text
        # print('최고온도 ' + max_tem + '에요')
        self.weather_data += '최고온도 ' + str(max_tem) + '에요. '

        # 체감온도
        sen_tem = info_list_li[1].find('span', {'class': 'sensible'}).text
        # print(sen_tem + '에요')
        self.weather_data += str(sen_tem) + '에요. '
        # rainfall = info_list_li[2].find('span',{'class':'rainfall'}).text
        # print(rainfall + ' 에요')

    def get_weather_detail(self, soup):
        # 날씨정보
        info_list = soup.find('ul', {'class': 'info_list'})
        info_list_li = info_list.findAll('li')
        cast_txt = info_list_li[0].text
        # print(cast_txt)
        self.weather_data += str(cast_txt) + ". "
        regex = re.compile("비|눈")
        search_str = regex.search(cast_txt)
        if search_str == '비':
            return 1
        elif search_str == '눈':
            return 2
        else:
            self.weather_data += "우산은 넣어둬요. "

    def get_weather_dust(self, soup):
        # 날씨 미세먼지, 오존지수
        detail_box = soup.find('div', {'class': 'detail_box'})
        # pprint(detail_box)
        detail_box_dd = detail_box.findAll('dd')

        # 미세먼지
        # fine_dust = detail_box_dd[0].find('span',{'class':'num'}).text #수치만 표시
        fine_dust = detail_box_dd[0].text  # 상태포함
        # print('미세먼지는 ' + fine_dust + ' 이에요')
        self.weather_data += '미세먼지는 ' + str(fine_dust) + ' 이에요. '

        # 초미세먼지
        # ultra_fine_dust = detail_box_dd[1].find('span',{'class':'num'}).text
        ultra_fine_dust = detail_box_dd[1].text
        # print('초미세먼지는 ' + ultra_fine_dust + ' 이에요')
        self.weather_data += '초미세먼지는 ' + str(ultra_fine_dust) + ' 이에요. '

        # 오존지수
        # ozone_index = detail_box_dd[2].find('span',{'class':'num'}).text
        ozone_index = detail_box_dd[2].text
        # print('오존지수는 ' + ozone_index + ' 이에요')
        self.weather_data += '오존지수는 ' + str(ozone_index) + ' 이에요. '

    def print_all_weather(self, soup):
        # 모든 날씨 정보 표시
        self.get_today_tem(soup)
        self.get_weather_detail(soup)
        self.get_weather_dust(soup)