import requests
from bs4 import BeautifulSoup
import copy
import json
import sched, time
# import sys, os
# sys.path.append(os.pardir)

def koushin( keyword="주요뉴스"):
    articleDics = {}
    sidSet = {"정치":"100", "경제":"101", "사회":"102", "생활":"103", "세계":"104", "IT":"105"}
    #tempList=[]
    #keyword = input("분야를 선택하세요.\n주요뉴스 / 정치 / 경제 / 사회 / 생활 / 세계 / IT: ")
    if keyword == "주요뉴스":
        url = "https://m.news.naver.com/rankingList.nhn"
    else:
        url = "https://m.news.naver.com/rankingList.nhn?sid1="+sidSet[keyword]
    print(url)
    raw = requests.get(url, 
                        headers={'User-Agent':'Mozilla/5.0 (Linux; Android 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("div.ranking_news > ul > li")

    for arti in articles:
        title = arti.select_one("div.commonlist_tx_headline").text
        for link in arti.findAll("a"):
            if 'href' in link.attrs: # 내부에 있는 항목들을 리스트로 가져옵니다 ex) {u'href': u'//www.wikimediafoundation.org/'}
                #print (link.attrs['href'])
                #articleDics[title] =link.attrs['href']

                linkAddress = link.attrs['href']
                
                # 링크 가지고 페이지 로드, 파싱.
                raw = requests.get("https://m.news.naver.com"+linkAddress,
                        headers={'User-Agent':'Mozilla/5.0 (Linux; Android 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'})
                html = BeautifulSoup(raw.text, "html.parser")

                # 받아온 html 파싱된 거에서 div#contents 하나 선택.
                articleContent = str(html.select_one("div#contents"))
                
                #마지막으로 {(주소):[(제목),(본문)]}
                articleDics[linkAddress] = [title,articleContent]
    return articleDics

def koushinReturnsList( keyword="주요뉴스"):
    result = []
    articleLinkList = []
    articleTitleList = []
    articleViewCountList = []
    articleContentList = []
    sidSet = {"정치":"100", "경제":"101", "사회":"102", "생활":"103", "세계":"104", "IT":"105"}
    #tempList=[]
    #keyword = input("분야를 선택하세요.\n주요뉴스 / 정치 / 경제 / 사회 / 생활 / 세계 / IT: ")
    if keyword == "주요뉴스":
        url = "https://m.news.naver.com/rankingList.nhn"
    else:
        url = "https://m.news.naver.com/rankingList.nhn?sid1="+sidSet[keyword]
    print(url)
    raw = requests.get(url, 
                        headers={'User-Agent':'Mozilla/5.0 (Linux; Android 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("div.ranking_news > ul > li")

    # article들 <li>목록에서 하나 선택.
    for arti in articles:
        # 제목 뽑기
        title = arti.select_one("div.commonlist_tx_headline").text
        # 조회수 뽑기
        tmp = arti.select_one("div.commonlist_tx_visit")
        for child in tmp.find_all('span'):
            child.decompose()
        viewCount = tmp.text.strip()

        # <a>에서 href(하나) 뽑기
        for link in arti.findAll("a"):
            if 'href' in link.attrs: # 내부에 있는 항목들을 리스트로 가져옵니다 ex) {u'href': u'//www.wikimediafoundation.org/'}

                linkAddress = link.attrs['href']
                
                # 링크 가지고 페이지 로드, 파싱.
                raw = requests.get("https://m.news.naver.com"+linkAddress,
                        headers={'User-Agent':'Mozilla/5.0 (Linux; Android 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'})
                html = BeautifulSoup(raw.text, "html.parser")

                # 뉴스 본문 뽑기. 받아온 html 파싱된 거에서 기사 제목+내용 선택.
                articleTitle = html.select_one("div.media_end_head")
                articleBody = html.select_one("div.newsct_article._news_article_body")

                articleContent = (str(articleTitle) + str(articleBody))

        articleLinkList.append(linkAddress)
        articleTitleList.append(title)
        articleViewCountList.append(viewCount)
        articleContentList.append(articleContent)
    result.append(articleLinkList)
    result.append(articleTitleList)
    result.append(articleViewCountList)
    result.append(articleContentList)

    return result

def refreshJson():
    with open('news/static/headline.json', 'w') as fp:
        json.dump(koushin(), fp)
    with open('news/static/politics.json', 'w') as fp:
        json.dump(koushin('정치'), fp)
    with open('news/static/economic.json', 'w') as fp:
        json.dump(koushin('경제'), fp)
    with open('news/static/social.json', 'w') as fp:
        json.dump(koushin('사회'), fp)
    with open('news/static/living.json', 'w') as fp:
        json.dump(koushin('생활'), fp)
    with open('news/static/globalNews.json', 'w') as fp:
        json.dump(koushin('세계'), fp)
    with open('news/static/it.json', 'w') as fp:
        json.dump(koushin('IT'), fp)
    print("크롤러 실행완료 - "+ returnNowTimeToString() )

def refreshListToJson():
    tmpList = koushinReturnsList();
    with open('news/static/headline-link.json', 'w') as fp:
        json.dump(tmpList[0], fp)
    with open('news/static/headline-title.json', 'w') as fp:
        json.dump(tmpList[1], fp)
    with open('news/static/headline-viewCount.json', 'w') as fp:
        json.dump(tmpList[2], fp)
    with open('news/static/headline-content.json', 'w') as fp:
        json.dump(tmpList[3], fp)
    
    tmpList = koushinReturnsList('정치');
    with open('news/static/politics-link.json', 'w') as fp:
        json.dump(tmpList[0], fp)
    with open('news/static/politics-title.json', 'w') as fp:
        json.dump(tmpList[1], fp)
    with open('news/static/politics-viewCount.json', 'w') as fp:
        json.dump(tmpList[2], fp)
    with open('news/static/politics-content.json', 'w') as fp:
        json.dump(tmpList[3], fp)

    tmpList = koushinReturnsList('경제');
    with open('news/static/economic-link.json', 'w') as fp:
        json.dump(tmpList[0], fp)
    with open('news/static/economic-title.json', 'w') as fp:
        json.dump(tmpList[1], fp)
    with open('news/static/economic-viewCount.json', 'w') as fp:
        json.dump(tmpList[2], fp)
    with open('news/static/economic-content.json', 'w') as fp:
        json.dump(tmpList[3], fp)

    tmpList = koushinReturnsList('사회');
    with open('news/static/social-link.json', 'w') as fp:
        json.dump(tmpList[0], fp)
    with open('news/static/social-title.json', 'w') as fp:
        json.dump(tmpList[1], fp)
    with open('news/static/social-viewCount.json', 'w') as fp:
        json.dump(tmpList[2], fp)
    with open('news/static/social-content.json', 'w') as fp:
        json.dump(tmpList[3], fp)

    tmpList = koushinReturnsList('생활');
    with open('news/static/living-link.json', 'w') as fp:
        json.dump(tmpList[0], fp)
    with open('news/static/living-title.json', 'w') as fp:
        json.dump(tmpList[1], fp)
    with open('news/static/living-viewCount.json', 'w') as fp:
        json.dump(tmpList[2], fp)
    with open('news/static/living-content.json', 'w') as fp:
        json.dump(tmpList[3], fp)

    tmpList = koushinReturnsList('세계');
    with open('news/static/globalNews-link.json', 'w') as fp:
        json.dump(tmpList[0], fp)
    with open('news/static/globalNews-title.json', 'w') as fp:
        json.dump(tmpList[1], fp)
    with open('news/static/globalNews-viewCount.json', 'w') as fp:
        json.dump(tmpList[2], fp)
    with open('news/static/globalNews-content.json', 'w') as fp:
        json.dump(tmpList[3], fp)

    tmpList = koushinReturnsList('IT');
    with open('news/static/it-link.json', 'w') as fp:
        json.dump(tmpList[0], fp)
    with open('news/static/it-title.json', 'w') as fp:
        json.dump(tmpList[1], fp)
    with open('news/static/it-viewCount.json', 'w') as fp:
        json.dump(tmpList[2], fp)
    with open('news/static/it-content.json', 'w') as fp:
        json.dump(tmpList[3], fp)
    print("크롤러 실행완료 - "+ returnNowTimeToString() )

def returnNowTimeToString():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s

def openJsonFileToList():
    with open('news/static/headline-link.json', 'r') as f:
        json_data_link = json.load(f)
    with open('news/static/headline-title.json', 'r') as f:
        json_data_title = json.load(f)
    with open('news/static/headline-viewCount.json', 'r') as f:
        json_data_viewCount = json.load(f)
    with open('news/static/headline-content.json', 'r') as f:
        json_data_content = json.load(f)
    # print(type(json_data_link))
    # print(type(json_data_title))
    # print(type(json_data_viewCount))
    # print(type(json_data_content))
    # print(json_data_link)
    # print(json_data_title)
    # print(json_data_viewCount)
    # print(json_data_content)

def generateTitleText():
    with open('news/static/politics-title.json', 'r') as f:
        titleList = json.load(f)[:10]
    with open('news/static/economic-title.json', 'r') as f:
        titleList = titleList + json.load(f)[:10]
    with open('news/static/social-title.json', 'r') as f:
        titleList = titleList + json.load(f)[:10]
    with open('news/static/living-title.json', 'r') as f:
        titleList = titleList + json.load(f)[:10]
    with open('news/static/globalNews-title.json', 'r') as f:
        titleList = titleList + json.load(f)[:10]
    with open('news/static/it-title.json', 'r') as f:
        titleList = titleList + json.load(f)[:10]
    return titleList

tmpInt = 0
for g in generateTitleText():
    tmpInt +=1
    print(str(tmpInt)+". "+g)

timeout = 120

starttime=time.time()
while True:
    print("tick!")
    refreshListToJson()
    time.sleep(timeout - ((time.time() - starttime) % timeout))
    print("Crawling Done!!")


# for k in articleDics.keys():
#     print(k)
# for v in articleDics.values():
#     print(v)
#     input('계속?')
