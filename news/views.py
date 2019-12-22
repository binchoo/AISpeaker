import os
import json
from django import template
from django.http import HttpResponse
from django.shortcuts import render
from google.cloud import texttospeech
#from google.cloud import storage
from google.oauth2 import service_account


GOOGLE_APPLICATION_CREDENTIALS = './voiceauth.json'

# Create your views here.
def home(request):
    return render(request, 'index.html')

def test(request):
    with open('news/static/headline.json', 'r') as f:
        json_data = json.load(f)
    return render(request, 'test.html', {'asdfg':json_data})

def stringListContainsIndex(lst, stri):
    # 입력받은 리스트 lst, 스트링 stri에서, 리스트의 몇 번째 원소가 stri를 포함하는지 검색.
    # 있으면 index(int) 반환. index는 0부터 시작.
    # 없으면 -1 반환.
    tmpInt = 0
    for l in lst:
        if stri in l:
            return tmpInt
        else:
            tmpInt = tmpInt + 1
    return -1

# def headlines(request):
#     with open('news/static/headline.json', 'r') as f:
#         json_data = json.load(f)
#     return render(request, '주요 뉴스.html', {'asdfgk':list(json_data.keys())}, {'asdfgvl':json_data.values()})
## 주요 뉴스.html ##
def headlines(request):
    news_title_text = generateTitleText()
    with open('news/static/headline-link.json', 'r') as f:
        json_data_link = json.load(f)
    with open('news/static/headline-title.json', 'r') as f:
        json_data_title = json.load(f)
    with open('news/static/headline-viewCount.json', 'r') as f:
        json_data_viewCount = json.load(f)
    with open('news/static/headline-content.json', 'r') as f:
        json_data_content = json.load(f)
    return render(request, '주요 뉴스.html', {'asdflink':json_data_link , 'asdfview':json_data_viewCount , 'asdftitl':json_data_title, 'asdfcont':json_data_content, 'news_title_text': news_title_text})

## 분야별 랭킹 뉴스.html ##
def rankings(request):
    sid = {"정치":"politics", "경제":"economic", "사회":"social", "생활":"living", "세계":"globalNews", "IT":"it"}
    division = request.GET['division'] # division 값: 정치 / 경제 / 사회 / 생활 / 세계 / IT
    
    with open('news/static/'+sid[division]+'-link.json', 'r') as f:
        json_data_link = json.load(f)
    with open('news/static/'+sid[division]+'-title.json', 'r') as f:
        json_data_title = json.load(f)
    with open('news/static/'+sid[division]+'-viewCount.json', 'r') as f:
        json_data_viewCount = json.load(f)
    with open('news/static/'+sid[division]+'-content.json', 'r') as f:
        json_data_content = json.load(f)

    return render(request, '분야별 랭킹 뉴스.html', {'division':division, 'asdflink':json_data_link, 'asdfview':json_data_viewCount , 'asdftitl':json_data_title, 'asdfcont':json_data_content})


## 기사 본문.html ##
def articleContent(request):
    sid1 = request.GET['sid1'] # sid1 값: 100 / 101 / 102 / 103 / 104 / 105 
    aid = request.GET['aid'] # aid 값(예시): 0000446610
    sidtoDivision = {"100":"politics", "101":"economic", "102":"social", "103":"living", "104":"globalNews", "105":"it"}
    
    with open('news/static/'+sidtoDivision[sid1]+'-link.json', 'r') as f:
        json_data_link = json.load(f)
    with open('news/static/'+sidtoDivision[sid1]+'-content.json', 'r') as f:
        json_data_content = json.load(f)
    
    #  기사링크 리스트에서 aid 포함되는 문자열 있는지, 있으면 몇 번째인지 검색
    index = stringListContainsIndex(json_data_link,aid)
    
    if(index < 0):
        print("기사 없음 - 오류!")
        return -1
    print(str(index)+'번째 기사 출력!')
    return render(request, '기사 본문.html', \
        {'sid1':sid1, 'aid':aid, 'contentElement':json_data_content[index]})

## 오디오파일 mp3 응답 ##        
def respondAudioFile(request):
    textQuery = request.GET['textQuery'] # tts에 들어갈 글 
    
    ttsAudio = generateMP3(textQuery)
    response = HttpResponse(ttsAudio)
    response['Content-Type'] ='audio/mp3'
    return response

def generateTitleText():
    with open('news/static/politics-title.json', 'r') as f:
        titleList = str(json.load(f)[:2])+". "
    with open('news/static/economic-title.json', 'r') as f:
        titleList = titleList + str(json.load(f)[:2])+". "
    with open('news/static/social-title.json', 'r') as f:
        titleList = titleList + str(json.load(f)[:2])+". "
    with open('news/static/living-title.json', 'r') as f:
        titleList = titleList + str(json.load(f)[:2])+". "
    with open('news/static/globalNews-title.json', 'r') as f:
        titleList = titleList + str(json.load(f)[:2])+". "
    with open('news/static/it-title.json', 'r') as f:
        titleList = titleList + str(json.load(f)[:2])+". "
    return titleList

def generateMP3(contents):
    #credentials = service_account.Credentials.from_service_account_file('./voiceauth.json')

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.types.SynthesisInput(text=contents)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='ko-KR',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL,
        name = "ko-KR-Wavenet-C")

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        pitch = 4)

    response = client.synthesize_speech(synthesis_input, voice, audio_config)
        
    return response.audio_content

