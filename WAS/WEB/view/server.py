from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from .WebCamera.ssdNet import ssdNet
from .VideoCamera import VideoCamera

cam = VideoCamera()
class View:
    # url mapping
    def server(request, hw, dl):
        print("hw :", hw, "  dl:",dl)
        import socket
        import requests
        import re

        print("내부 ip : ",socket.gethostbyname(socket.gethostname()))
        ip = socket.gethostbyname(socket.gethostname())

        req = requests.get("http://ipconfig.kr")

        print("외부 IP : ", re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1])
        outip = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]

        page = 'server'
        context = {
            'page': page,
            'ip' : ip,
            'outip' : outip,
        }
        if hw == "master" and dl == "page":
            return render(request, './0_SERVER/1_master.html', context)
        elif hw == "proxy" and dl == "page":
            return render(request, './0_SERVER/2_proxy.html', context)
        elif hw == "turtlebot" and dl == "page":
            return render(request, './0_SERVER/3_turtlebot.html', context)
        elif hw == "WebCamera" and dl =="ObjectDetection":
            return render(request, './0_SERVER/WebCamera/ObjectDetection.html', context)
        elif hw == "WebCamera" and dl == "gesture-recognition":
            return render(request, './0_SERVER/WebCamera/gesture-recognition.html', context)
        elif hw == "WebCamera" and dl == "MaskDetection":
            return render(request, './0_SERVER/WebCamera/MaskDetection.html', context)
        elif hw == "WebCamera" and dl == "FireDetection":
            return render(request, './0_SERVER/WebCamera/FireDetection.html', context)

    def webCam(request):
        global cam
        try:
            video = StreamingHttpResponse(
                gen(cam, "webcam"), content_type="multipart/x-mixed-replace;boundary=frame")
            return video
        except:  # This is bad! replace it with proper handling
            print("Exception Error. webCam")
            pass

    def deeplearning(request, model):
        print('model :', model)
        global cam
        try:
            # ssdNet = VideoCamera()
            # grabbed, frame = ssdNet.read()
            video = StreamingHttpResponse(
                gen(cam, model), content_type="multipart/x-mixed-replace;boundary=frame")
            return video
        except:  # This is bad! replace it with proper handling
            print("Exception Error. ssdNet")
            pass

def gen(camera,mod):
    print('gen() -mod :',mod)
    while True:
        frame = camera.get_frame(mod)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
