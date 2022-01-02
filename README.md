# 한국품질재단 AI 개발자 양성과정

AI PROJECT : AUTONOMOUS SURVEILLANCE ROBOT

자율 순찰 로봇

반장 : 김민서

팀장 : 김민서

팀원 : 한정탁, 이은창, 김경진

멘토 : 이성민(LG전자), 문새마로(TmaxSoft)

한줄평 : 내 인생에서 "차라리 일하고 말지.." 라는 생각이 들정도로 어렵고 시간도 부족하고 빡센 난이도 역대급이였던 프로젝트

# 사용기술
  
  1. 자율 주행
  2. TCP 소켓통신

    - 소켓통신을 이용한 이미지 송수신 API 모듈

  4. YOLO V5
  
    1). MASK DETECT
    
    2). FIRE DETECT
    
    3). GESTURE RECOGNITION - 모션 인식 컨트롤러 모듈
    
    4). SSDNET
    


# YOUTUBE

  최종프로젝트 시연 영상
  
  영상 기획&편집 : 이은창
  
  카메라 보조 : 김민서, 한정탁
  
  로봇 세팅 및 조종 : 한정탁
  
  보조출연 : 김민서
  
  https://www.youtube.com/watch?v=F3jz9fvuC3E
  

# 목차
  
  1.    CONTENS & GANTT CHART
  2.    ABSTRACT
  3.    ARCHITECTURE
  4.    TECHNOLOGIES
  5.    DEMONSTRATE

# PPT

![한국품질재단_최종프로젝트_4조_ASR_1](https://user-images.githubusercontent.com/46194003/147873923-d9dc00a5-df3a-4db1-8a0a-467c68b22b71.jpg)
![한국품질재단_최종프로젝트_4조_ASR_2](https://user-images.githubusercontent.com/46194003/147873925-b24fc242-889a-4d62-93c7-d7b9fd89f0c0.jpg)
![한국품질재단_최종프로젝트_4조_ASR_3](https://user-images.githubusercontent.com/46194003/147873926-2a587c62-4e4a-46db-b5c5-91a684ba5422.jpg)
![한국품질재단_최종프로젝트_4조_ASR_4](https://user-images.githubusercontent.com/46194003/147873930-7f6d0f6c-3357-450f-bcb8-b118497da3dd.jpg)
![한국품질재단_최종프로젝트_4조_ASR_5](https://user-images.githubusercontent.com/46194003/147873932-28ccc3fc-494c-49f7-b0fa-f90555523290.jpg)
![한국품질재단_최종프로젝트_4조_ASR_6](https://user-images.githubusercontent.com/46194003/147873933-212ae773-43ac-4940-816a-af26ee449e7b.jpg)
![한국품질재단_최종프로젝트_4조_ASR_7](https://user-images.githubusercontent.com/46194003/147873934-844628b4-61d0-4435-9810-75d292aea991.jpg)
![한국품질재단_최종프로젝트_4조_ASR_8](https://user-images.githubusercontent.com/46194003/147873935-6bd9e302-b53a-4e15-a85b-98ab0f43ccdf.jpg)
![한국품질재단_최종프로젝트_4조_ASR_9](https://user-images.githubusercontent.com/46194003/147873936-454673d0-86f7-43c8-a297-21fa32ef6994.jpg)
![한국품질재단_최종프로젝트_4조_ASR_10](https://user-images.githubusercontent.com/46194003/147873937-5b239a10-cca8-44a5-81bd-f55346860440.jpg)
![한국품질재단_최종프로젝트_4조_ASR_11](https://user-images.githubusercontent.com/46194003/147873938-5486d606-022f-498e-95c6-01ad9f1de0be.jpg)
![한국품질재단_최종프로젝트_4조_ASR_12](https://user-images.githubusercontent.com/46194003/147873939-89b63398-d70a-49b6-b54b-32eaada35bc3.jpg)
![한국품질재단_최종프로젝트_4조_ASR_13](https://user-images.githubusercontent.com/46194003/147873940-cd063e6c-9ee6-47af-b3f1-69ef8950917e.jpg)
![한국품질재단_최종프로젝트_4조_ASR_14](https://user-images.githubusercontent.com/46194003/147873941-64492195-5a09-4071-bfc5-ce6314a8b147.jpg)
![한국품질재단_최종프로젝트_4조_ASR_15](https://user-images.githubusercontent.com/46194003/147873942-c54551fc-ba4b-4a80-a5ab-485982d4037a.jpg)
![한국품질재단_최종프로젝트_4조_ASR_16](https://user-images.githubusercontent.com/46194003/147873943-5f6a74ee-e451-4e4d-8c14-320fd7ac5aaf.jpg)
![한국품질재단_최종프로젝트_4조_ASR_17](https://user-images.githubusercontent.com/46194003/147873944-f7002389-1481-494c-90e7-ed9f3fb3e497.jpg)
![한국품질재단_최종프로젝트_4조_ASR_18](https://user-images.githubusercontent.com/46194003/147873945-ae2d1072-95e1-4660-bea0-1c4ef967605b.jpg)
![한국품질재단_최종프로젝트_4조_ASR_19](https://user-images.githubusercontent.com/46194003/147873946-f8474a3f-0844-4859-a2aa-a4b568edf88e.jpg)
![한국품질재단_최종프로젝트_4조_ASR_20](https://user-images.githubusercontent.com/46194003/147873947-0341793f-5d59-43c6-8146-a38dca141286.jpg)
![한국품질재단_최종프로젝트_4조_ASR_21](https://user-images.githubusercontent.com/46194003/147873948-7e5a2b19-3f00-42bd-8a32-60ec193495f7.jpg)


# GIT

git init : 현재 파일을 깃허브와 연동

git remote add origin https://github.com/IIBlackCode/KFQ_FinalProject.git : 깃허브 오리진에 추가

git remote -v : 연결확인

git pull origin main - 깃허브 소스 내려받기

git add . - 로컬소스 스테이징

git commit -m "커밋내용" - 커밋

git checkout master - master로 ?

git merge MS-K - MS-K 브릿지와 master 브릿지 merge

git push origin master - 최종적으로 깃허브에 업로드

MERGE 작업 방법 모터 - 속도파악 라이다 - 주변사물 IMU 센서 - 속도/위치 정보 카메라 - 영상 정보

git pull origin master

git pull origin fire

git pull origin mask

git checkout master

git merge origin/mask

git merge origin/fire

git add .

git commit -m "merge"

git push origin master
