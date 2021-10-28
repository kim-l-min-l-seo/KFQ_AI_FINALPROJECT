import cv2
import threading

#WebCamera Version Module import
from .WebCamera.ssdNet import ssdNet
from .WebCamera.gesture_recognition import Gesture_recognition
from .WebCamera.MaskDetection import maskDetection

class VideoCamera(object):
    def __init__(self):
        # 실시간 영상캡처 및 Thread 시작
        self.video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self, mod):
        image = None
        if mod == "webcam":
            image = self.frame
        elif mod == "ObjectDetection":
            image = ssdNet(self.frame)
        elif mod == "gesture-recognition":
            image = Gesture_recognition()
            image = image.gesture_recognition(self.frame)
        elif mod == "MaskDetection":
            image = maskDetection(self.frame)

        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
