# IMAGE 수신 모듈
# -------------------------- 2021 - 11 - 01 -------------------------- #
# ***************** imageAPI_client.py module issue ****************** #
# log 추가 - # Document > MODULE > IMAGE_API > test.py 참고하여 파일기록으로 추후 전환
# LOG를 logging으로 찍으면 프래임깨짐이 없음
# LOG를 logger로 변경하면 프래임드랍 발생
# -------------------------- -------------- -------------------------- #

from ctypes import sizeof
import socket
import cv2
import time
from datetime import datetime
import numpy
import base64
import threading

import logging

#WebCamera Version Module import
from .TurtlebotCamera.ssdNet import ssdNet
from .TurtlebotCamera.gesture_recognition import Gesture_recognition
from .TurtlebotCamera.MaskDetection import maskDetection
from .TurtlebotCamera.FireDetection import deepfire_CV

stringData = None
gsock = None
class ServerSocket:
    
    def __init__(self, ip, port):
        global gsock
        self.TCP_IP = ip
        self.TCP_PORT = port
        if gsock == None:
            self.socketOpen()
        else:
            print("gsock is not None : ",gsock)
        self.receiveThread = threading.Thread(target=self.receiveImages)
        self.receiveThread.start()

    def socketClose(self):
        global gsock
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')
        self.sock = None
        gsock = None

    def socketOpen(self):
        global gsock
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gsock = self.sock
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(0)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        if gsock == None :
            print("gsock is None")
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')
    
    def receiveImages(self, model):
        global stringData
        try:
            while True:
                length = self.recvall(self.conn, 64)
                length1 = length.decode('utf-8')
                stringData = self.recvall(self.conn, int(length1))
                data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)

                # 실수로 지웠던 image Decode 복구 : 저 과정을 거쳐야 원본파일로 복구되는듯
                # jpg > imincode 송신 >>> 수신 > imdecode > jpg
                # decode가 없으면 1차원배열로 떨어짐 - DL적용 불가

                frame = cv2.imdecode(data, 1)
                # cv2.imshow("image", frame)
                # print("frame.shape",frame.shape)
                # print("type of frame",type(frame))
                
                try:
                    if model == "webcam":
                        pass
                    elif model == "ObjectDetection":
                        frame = ssdNet(frame)
                    elif model == "gesture-recognition":
                        image = Gesture_recognition()
                        frame = image.gesture_recognition(frame)
                    elif model == "MaskDetection":
                        frame = maskDetection(frame)
                    elif model == "FireDetection":
                        frame = deepfire_CV(frame)
                except Exception as e:
                    print("exception >>>", e)
                    pass

                _, jpeg = cv2.imencode('.jpg', frame)
                return jpeg.tobytes()
        except Exception as e:
            # logging.warning("exception >>>>",e)
            if gsock == None:
                self.socketClose()
                self.socketOpen()
                self.receiveThread = threading.Thread(target=self.receiveImages)
                self.receiveThread.start()
            else:
                logging.info("gsock is not None : ", gsock)
                pass

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
