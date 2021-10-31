from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_GET, require_POST

import cv2
import threading
import socket
import numpy as np

from .VideoCamera import VideoCamera
from .imageAPI_client import ServerSocket

# Stream에 로그 기록
import logging
# logging.basicConfig(filename='ImageAPI.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# loghandler 생성
streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler('ImageAPI.log')

# logger instance 설정
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

# logger instance level 설정
logger.setLevel(level=logging.WARNING)

# Local Camera
cam = VideoCamera()
ip = '192.168.219.100'
socket = ServerSocket(ip, 9090)

# -------------------------------------------------- #
# 2021 - 11 - 01
# ***** server.py module issue *****
# [socket = ServerSocket(ip, 9090)] 관련
# 이미지를 수신하는 PAGE에서 소켓에 접속하는 구조로 변경시
# 해당 PAGE로 접속할 때 마다 소켓에 중복접근 - PAGE RELOAD 불가

# WEB 실행시 단 한번만 소켓에 접근하고 그 이후는 연결하지 않도록 변경
# PAGE RELOAD 가능, RELOAD TEST중 FRAME이 깨지는 현상을 분석하기 위해
# LOG를 추가하였고 level 단위를 WARNING 지정 및 로그 분석 후 주석처리
# 주석처리 후 FRAME 깨짐현상 없어짐 - 원인분석中 ...

class View:
    # url mapping
    def server(request, hw, dl):
        global ip
        logging.info("hw :", hw, "  dl:", dl)
        import requests
        import re

        logging.info("내부 ip : ", ip)
        req = requests.get("http://ipconfig.kr")


        page = 'server'
        context = {
            'page': page,
            'ip' : ip,
            # 'outip' : outip,
        }

        if hw == "master" and dl == "page":
            return render(request, './0_SERVER/1_master.html', context)
        elif hw == "proxy" and dl == "page":
            return render(request, './0_SERVER/2_proxy.html', context)
        elif hw == "videotest" and dl == "page":
            return render(request, './0_SERVER/3_videotest.html', context)
        elif hw == "template" and dl == "page":
            return render(request, './0_SERVER/4_template.html', context)
        elif hw == "template2" and dl == "page":
            return render(request, './0_SERVER/5_template_2.html', context)

        # WebCamera
        elif hw == "WebCamera" and dl =="none":
            return render(request, './0_SERVER/WebCamera/WebCameraTest.html', context)
        elif hw == "WebCamera" and dl =="ObjectDetection":
            return render(request, './0_SERVER/WebCamera/ObjectDetection.html', context)
        elif hw == "WebCamera" and dl == "gesture-recognition":
            return render(request, './0_SERVER/WebCamera/gesture-recognition.html', context)
        elif hw == "WebCamera" and dl == "MaskDetection":
            return render(request, './0_SERVER/WebCamera/MaskDetection.html', context)
        elif hw == "WebCamera" and dl == "FireDetection":
            return render(request, './0_SERVER/WebCamera/FireDetection.html', context)

        # Turtlebot
        elif hw == "Turtlebot" and dl == "none":
            return render(request, './0_SERVER/Turtlebot/TurtlebotCameraTest.html', context)
        elif hw == "Turtlebot" and dl =="ObjectDetection":
            return render(request, './0_SERVER/Turtlebot/ObjectDetection.html', context)
        elif hw == "Turtlebot" and dl == "gesture-recognition":
            return render(request, './0_SERVER/Turtlebot/gesture-recognition.html', context)
        elif hw == "Turtlebot" and dl == "MaskDetection":
            return render(request, './0_SERVER/Turtlebot/MaskDetection.html', context)
        elif hw == "Turtlebot" and dl == "FireDetection":
            return render(request, './0_SERVER/Turtlebot/FireDetection.html', context)

    def webCamera(request, model):
        global cam
        logging.info('model :', model)
        try:
            video = StreamingHttpResponse(
                frame_webCamera(cam, model), content_type="multipart/x-mixed-replace;boundary=frame")
            return video
        except:  # This is bad! replace it with proper handling
            logging.info("Exception Error. webCamera")
            pass
    
    #Turtlebot Camera URL
    def imageAPI_Client(request, model):
        global ip, socket
        # socket = ServerSocket('192.168.43.130', 9090)
        # socket = ServerSocket(ip, 9090)
        if request.method == 'POST':
            logging.info(" POST METHOD ")
        else :
            try :
                video = StreamingHttpResponse(
                    frame_turtlebot(model, socket), content_type="multipart/x-mixed-replace;boundary=frame")
                return video
            except :  # This is bad! replace it with proper handling
                print("Exception Error. imageAPI_Client")
                pass

# 터틀봇으로부터 이미지 수신
def frame_turtlebot(model, socket):
    global count
    global server
    logging.info("Turtlebot model : ", model)
        
    while True:
        try :
            frame = socket.receiveImages(model)
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except Exception as e :
            # print("frame_turtlebot exception >>",e)
            pass

# Local Camera Frame
def frame_webCamera(camera,mod):
    logging.info('gen() -mod :', mod)
    while True:
        # frame = video.read()
        frame = camera.get_frame(mod)
        # if mod == "webcam":
            # print("mod  :",mod,"   FRAME type : ",type(frame))
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
