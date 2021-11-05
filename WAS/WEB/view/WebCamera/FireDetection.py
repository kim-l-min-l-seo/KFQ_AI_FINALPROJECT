from django.contrib import messages
import cv2
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox


def deepfire_CV(frame):
    fire_cascade = cv2.CascadeClassifier(os.getcwd()+"\WEB\\"+"view\WebCamera\models\\"+"fire_detection.xml")
    # cap = cv2.VideoCapture(0)
    while (True):
        # ret, frame = cap.read()
        fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

        for (x, y, w, h) in fire:
            cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
            # roi_gray = gray[y:y + h, x:x + w]
            # roi_color = frame[y:y + h, x:x + w]
            print("불 감지")
            messagebox.showwarning("<경고>","화재가 발생했습니다.")
        return frame
    