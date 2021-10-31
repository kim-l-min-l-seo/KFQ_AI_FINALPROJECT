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

# Local Camera
cam = VideoCamera()
ip = '192.168.219.100'
print("server.py")
socket = ServerSocket(ip, 9090)
# server = ServerSocket('192.168.219.104', 9090)
class View:
    # url mapping
    def server(request, hw, dl):
        global ip
        print("hw :", hw, "  dl:",dl)
        import requests
        import re

        # ip = socket.gethostbyname(socket.gethostname())
        # ip = '192.168.43.130'
        print("내부 ip : ",ip)
        req = requests.get("http://ipconfig.kr")

        # print("외부 IP : ", re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1])
        # outip = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]

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


    # def webCam(request):
    #     global cam
    #     try:
    #         video = StreamingHttpResponse(
    #             gen(cam, "webcam"), content_type="multipart/x-mixed-replace;boundary=frame")
    #         return video
    #     except:  # This is bad! replace it with proper handling
    #         print("Exception Error. webCam")
    #         pass

    def webCamera(request, model):
        print('model :', model)
        global cam
        try:
            video = StreamingHttpResponse(
                frame_webCamera(cam, model), content_type="multipart/x-mixed-replace;boundary=frame")
            return video
        except:  # This is bad! replace it with proper handling
            print("Exception Error. webCamera")
            pass
    
    #Turtlebot Camera URL
    def imageAPI_Client(request, model):
        global ip, socket
        # socket = ServerSocket('192.168.43.130', 9090)
        # socket = ServerSocket(ip, 9090)
        if request.method == 'POST':
            print(" POST METHOD ")
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
    print("Turtlebot model : ", model)
        
    while True:
        frame = socket.receiveImages(model)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Local Camera Frame
def frame_webCamera(camera,mod):
    print('gen() -mod :',mod)
    while True:
        # frame = video.read()
        frame = camera.get_frame(mod)
        # if mod == "webcam":
            # print("mod  :",mod,"   FRAME type : ",type(frame))
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
