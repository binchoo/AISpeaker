# AISpeaker



## 서비스 실행 방법

AISpeaker 프로젝트 폴더가 보이는 위치에서 아래 명령을 실행합니다. 

```bash
docker service createdocker service create —name aispeaker –p 8000:8000 —mount “type=bind.src=$(pwd)/AISpeaker,dst=/myservice” xentai/aispeaker
```

## 서비스 접속 방법

로컬에서 구동된 서비스는 아래 주소로 들어갑니다.

```http
http://127.0.0.1:8000
```

저희 팀이 배포한 서비스는 아래 주소로 접속합니다.

```http
https://bquadai.asdv.cf
```

## 서비스 종료 방법

```bash
docker service rm aispeaker
```
