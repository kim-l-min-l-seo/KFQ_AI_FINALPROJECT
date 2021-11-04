from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_GET, require_POST
import cv2
import threading
from yolov5 import detect
from yolov5 import FireDetection

import socket
import numpy as np

# Stream에 로그 기록
import logging

# import camera driver
from importlib import import_module
import os
from base_camera import BaseCamera

def test(self, *args, **kwargs):
    # img_id = kwargs.get("id")
    # image_qs = ImageFile.objects.get(id=img_id)
    frame = detect.run(source='http://172.30.1.36:8000/web/WebCamera/webcam')
    try:
        # video = StreamingHttpResponse(frame, content_type="multipart/x-mixed-replace;boundary=frame")
        # return video
        return 
    except:  # This is bad! replace it with proper handling
        print("Exception Error. webCamera")
        pass

def test2(self, *args, **kwargs):
    # img_id = kwargs.get("id")
    # image_qs = ImageFile.objects.get(id=img_id)
    frame = FireDetection.run(source='http://172.30.1.36:8000/web/WebCamera/webcam')
    try:
        video = StreamingHttpResponse(frame, content_type="multipart/x-mixed-replace;boundary=frame")
        return video
        # return 
    except:  # This is bad! replace it with proper handling
        print("Exception Error. webCamera")
        pass

# def gen(camera):
#     """Video streaming generator function."""
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    if request.method == 'POST':
            logging.info(" POST METHOD ")
    else :
        try :
            frame = FireDetection.run(source='http://192.168.43.107:8000/web/TurtlebotCamera/webcam/')
            """Video streaming route. Put this in the src attribute of an img tag."""
            return StreamingHttpResponse(frame,
                content_type='multipart/x-mixed-replace; boundary=frame')
        except :  # This is bad! replace it with proper handling
            print("Exception Error. imageAPI_Client")
            pass

def fire_detection(request):
    if request.method == 'POST':
            logging.info(" POST METHOD ")
    else :
        try :
            frame = detect.run(source='http://192.168.43.107:8000/web/TurtlebotCamera/webcam/',weights='yolov5/fire_detection.pt')
            """Video streaming route. Put this in the src attribute of an img tag."""
            return StreamingHttpResponse(frame,
                content_type='multipart/x-mixed-replace; boundary=frame')
        except :  # This is bad! replace it with proper handling
            print("Exception Error. imageAPI_Client")
            pass