import cv2
import threading

#WebCamera Version Module import
from .WebCamera.ssdNet import ssdNet
from .WebCamera.gesture_recognition import gesture_recognition
from .WebCamera.MaskDetection import maskDetection
from .WebCamera.FireDetection import deepfire_CV

class VideoCamera(object):
    def __init__(self):
        # 실시간 영상캡처 및 Thread 시작
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self, mod):
        image = None
        if mod == "webcam":
            # print("self.frame : ", type(self.frame))
            # print("self.frame : ", self.frame.shape)
            image = self.frame
        elif mod == "ObjectDetection":
            image = ssdNet(self.frame)
        elif mod == "gesture-recognition":
            image = gesture_recognition(self.frame)
        elif mod == "MaskDetection":
            image = maskDetection(self.frame)
        elif mod == "FireDetection":
            image = deepfire_CV(self.frame)

        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
