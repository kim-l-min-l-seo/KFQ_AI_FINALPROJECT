from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from yolov5 import detect

def test(self, *args, **kwargs):
    # img_id = kwargs.get("id")
    # image_qs = ImageFile.objects.get(id=img_id)
    frame = detect.run(source='http://192.168.0.14:8000/web/WebCamera/webcam')
    try:
        video = StreamingHttpResponse(frame, content_type="multipart/x-mixed-replace;boundary=frame")
        return video
    except:  # This is bad! replace it with proper handling
        print("Exception Error. webCamera")
        pass