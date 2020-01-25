# AISpeaker

## 알림사항

- 구글 음성 API의 사용권한 키가 도용되는 일로 구글 측에서 차단을 당했습니다. 따라서 텍스트를 읽어주는 구글 보이스를 현재 사용할 수 없습니다
- 해당 레포지토리의 AISpeaker는 모노리틱 구조이며 마이크로서비스로 변경하려면 Forwarder > Application.py 의 설정을 변경해야 합니다
- 성경 단락 QA는 빨간 버튼을 누르면 etri BERT를 사용합니다. dms 버튼을 누르면 dms BERT를 사용합니다
  - etri BERT는 본문길이에 제한이 생겼습니다. 그러므로 빨간 버튼을 사용할 때는 4~5절 정도의 본문에 대한 질문을 합시다
  - dms BERT는 본문길이에 제한이 없으나 그 결과물이 overlay view에 뿌려지지 않습니다. 개발자모드의 네트워크 수신 패킷을 보아 결과물을 확인할 수 있습니다. dms BERT의 결과물을 화면에 뿌리는 로직을 개발할 예정입니다.

## 서비스 실행, 접속, 종료

### 서비스 실행 방법

AISpeaker 프로젝트 폴더가 보이는 위치에서 아래 명령을 실행합니다. 

```bash
docker service create —name aispeaker –p 8000:8000 —mount “type=bind.src=$(pwd)/AISpeaker,dst=/myservice” xentai/aispeaker
```

### 서비스 접속 방법

로컬에서 구동된 서비스는 아래 주소로 들어갑니다.

```http
http://127.0.0.1:8000
```

저희 팀이 배포한 서비스는 아래 주소로 접속합니다.

```http
https://bquadai.asdv.cf
```

### 서비스 종료 방법

```bash
docker service rm aispeaker
```

## 프로젝트 폴더 구성

### 성경 애플리케이션

- 관여자 : binchoo, sangwoo

- [bible](https://github.com/binchoo/AISpeaker/tree/master/bible)

- Iterator, BatchIterator, BibleReader 클래스 구현함

### 뉴스 애플리케이션

- 관여자 : minseok

- [news](https://github.com/binchoo/AISpeaker/tree/master/news)

### 날씨 애플리케이션

- 관여자 : mingidi

- 유스케이스 구현량이 낮음

- [weather](https://github.com/binchoo/AISpeaker/tree/master/weather)

### 주식 애플리케이션

- 관여자 : binchoo

- 유스케이스 구현량이 낮음

- [stock](https://github.com/binchoo/AISpeaker/tree/master/stock)

### 명령 전달 애플리케이션

- 관여자 : binchoo, Lumy Kelvin, mingidi

- [Forwarder](https://github.com/binchoo/AISpeaker/tree/master/Forwarder)

- Forwarder, AppFactory, AppExceutor, Application 클래스 구현함

### 클라이언트 (html,css)
- 관여자 : Lumy Kelvin, Yewon Jeong
- [html](https://github.com/binchoo/AISpeaker/tree/master/speakerapp/templates)
- [js](https://github.com/binchoo/AISpeaker/tree/master/static/js)
- [css](https://github.com/binchoo/AISpeaker/tree/master/static/css)

### 명령 의도 파악기

- 관여자 : binchoo, sangwoo

- 모델 성능이 만족스럽지 않음

- [QuestionClassifier](https://github.com/binchoo/AISpeaker/tree/master/QuestionClassifier)

- [어텐션 모델](https://github.com/binchoo/AISpeaker/blob/master/speakerapp/question_classifier.py)

- 학습 레이블 : q.txt / a.txt

## 아키텍처 설명 자료

- [소설방 발표자료](https://drive.google.com/file/d/1oTqX2iZjI77aaep84KNxqaxkEoFCdRdW/view?usp=sharing)
- [소설방 보고서](https://drive.google.com/file/d/158pfaQDcUGcCsmSnZP_jNf2ylIhf4cyi/view?usp=sharing)


