# AISpeaker

## 알림사항

- 구글 음성 API의 사용권한 키가 도용되는 일로 구글 측에서 차단을 당했습니다 따라서 텍스트를 읽어주는 구글 보이스를 현재 사용할 수 없습니다
- 

## 서비스 실행, 접속, 종료

### 서비스 실행 방법

AISpeaker 프로젝트 폴더가 보이는 위치에서 아래 명령을 실행합니다. 

```bash
docker service createdocker service create —name aispeaker –p 8000:8000 —mount “type=bind.src=$(pwd)/AISpeaker,dst=/myservice” xentai/aispeaker
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

- 유스케이스 구현량 : 상

- [bible]: https://github.com/binchoo/AISpeaker/tree/master/bible

- Iterator, BatchIterator, BibleReader 클래스 구현함

### 뉴스 애플리케이션

- 관여자 : minseok

- 유스케이스 구현량 : 상

- [news]: https://github.com/binchoo/AISpeaker/tree/master/news

### 날씨 애플리케이션

- 관여자 : mingidi

- 유스케이스 구현량 : 중

- [weather]: https://github.com/binchoo/AISpeaker/tree/master/weather

### 주식 애플리케이션

- 관여자 : binchoo
- 유스케이스 구현량 : 하
- [stock]: https://github.com/binchoo/AISpeaker/tree/master/stock

### 명령 전달 애플리케이션

- 관여자 : binchoo
- 유스케이스 구현량 : 상
- [Forwarder]: https://github.com/binchoo/AISpeaker/tree/master/Forwarder
- Forwarder, AppFactory, AppExceutor, Application 클래스 구현함

### 명령 의도 파악기

- 관여자 : sangwoo
- 성능이 만족스럽지 않음
- [QuestionClassifier]: https://github.com/binchoo/AISpeaker/tree/master/QuestionClassifier
- 학습 레이블 : q.txt / a.txt
