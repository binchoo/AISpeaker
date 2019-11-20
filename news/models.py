from django.db import models
import copy
import requests
from bs4 import BeautifulSoup
#from inheritance import *

# Create your models here.
def koushin(url):
    articleDics = {}
    raw = requests.get(url,
                        headers={'User-Agent':'Mozilla/5.0 (Linux; Android 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("div.ranking_news > ul > li")

    for arti in articles:
        title = arti.select_one("div.commonlist_tx_headline").text
        for link in arti.findAll("a"):
            if 'href' in link.attrs: # 내부에 있는 항목들을 리스트로 가져옵니다 ex) {u'href': u'//www.wikimediafoundation.org/'}
                linkAddress = link.attrs['href']
                
                # 링크 가지고 페이지 로드, 파싱.
                raw = requests.get("https://m.news.naver.com"+linkAddress,
                        headers={'User-Agent':'Mozilla/5.0 (Linux; Android 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'})
                html = BeautifulSoup(raw.text, "html.parser")

                # 받아온 html 파싱된 거에서 div#contents 하나 선택.
                articleContent = html.select_one("div#contents")
                
                #마지막으로 {(주소):[(제목),(본문)]}
                articleDics[linkAddress] = [title,articleContent]
    return articleDics

class Articles:
    """Super Class"""

    sidSet = {"정치":"100", "경제":"101", "사회":"102", "생활":"103", "세계":"104", "IT":"105"}
    headlineArticlesDic = {}
    politicsArticlesDic = {}
    economicArticlesDic = {}
    socialArticlesDic = {}
    livingArticlesDic = {}
    globalArticlesDic = {}
    itArticlesDic = {}


    # def __init__(self):
    #     pass;

    def gangshin(self):
        self.headlineArticlesDic = koushin("https://m.news.naver.com/rankingList.nhn")
        self.politicsArticlesDic = koushin("https://m.news.naver.com/rankingList.nhn?sid1="+self.sidSet["정치"])
        self.economicArticlesDic = koushin("https://m.news.naver.com/rankingList.nhn?sid1="+self.sidSet["경제"])
        self.socialArticlesDic = koushin("https://m.news.naver.com/rankingList.nhn?sid1="+self.sidSet["사회"])
        self.livingArticlesDic = koushin("https://m.news.naver.com/rankingList.nhn?sid1="+self.sidSet["생활"])
        self.globalArticlesDic = koushin("https://m.news.naver.com/rankingList.nhn?sid1="+self.sidSet["세계"])
        self.itArticlesDic = koushin("https://m.news.naver.com/rankingList.nhn?sid1="+self.sidSet["IT"])

