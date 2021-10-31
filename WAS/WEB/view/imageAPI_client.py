# IMAGE 수신 모듈

from ctypes import sizeof
import socket
import cv2
import time
from datetime import datetime
import numpy
import base64
import threading

# Stream에 로그 기록
import logging
# logging.basicConfig(filename='ImageAPI.log', level=logging.INFO)
# logger = logging.getLogger(__name__)

# # loghandler 생성
# streamHandler = logging.StreamHandler()
# fileHandler = logging.FileHandler('ImageAPI.log')

# # logger instance 설정
# logger.addHandler(streamHandler)
# logger.addHandler(fileHandler)

# # logger instance level 설정
# logger.setLevel(level=logging.WARNING)


#WebCamera Version Module import
from .TurtlebotCamera.ssdNet import ssdNet
from .TurtlebotCamera.gesture_recognition import Gesture_recognition
from .TurtlebotCamera.MaskDetection import maskDetection

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

                # invalid literal for int() with base 10 exception
                # length1 = float(length1)
                length1 = int(length1)

                stringData = self.recvall(self.conn, int(length1))
                data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
                # print("stringData : ", len(data))
                
                try:
                    if model == "webcam":
                        data = ssdNet(data)
                        # pass
                    elif model == "ObjectDetection":
                        data = ssdNet(data)
                    elif model == "gesture-recognition":
                        image = Gesture_recognition()
                        image = image.gesture_recognition(data)
                    elif model == "MaskDetection":
                        data = maskDetection(data)
                    else:
                        pass
                except Exception as e:
                    logging.info("exception >>>", e)
                
                return data.tobytes()
        except Exception as e:
            # logging.warning("exception >>>>",e)
            if gsock == None:
                self.socketClose()
                self.socketOpen()
                self.receiveThread = threading.Thread(target=self.receiveImages)
                self.receiveThread.start()
            else:
                # print("gsock is not None : ",gsock)
                pass

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

# def main():
#     server = ServerSocket('192.168.0.212', 9090)

# if __name__ == "__main__":
#     main()
