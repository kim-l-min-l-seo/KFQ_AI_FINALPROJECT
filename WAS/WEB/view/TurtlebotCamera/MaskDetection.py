import tensorflow as tf
tf.debugging.set_log_device_placement(True)
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from tkinter import messagebox

def maskDetection(image):
    model = load_model(os.getcwd()+"\WEB\\" +"view\WebCamera\models\mask_detector.model")
    
    # facenet = cv2.dnn.readNet(os.getcwd()+"\WEB\view\WebCamera\models\deploy.prototxt", os.getcwd()+"\WEB\view\WebCamera\models\res10_300x300_ssd_iter_140000.caffemodel")
    facenet = cv2.dnn.readNetFromCaffe(os.getcwd()+"\WEB\\"+"view\WebCamera\models\deploy.prototxt",
                                       os.getcwd()+"\WEB\\"+"view\WebCamera\models\\"+"res10_300x300_ssd_iter_140000.caffemodel")

    # cap = cv2.VideoCapture(0)
    # ret, img = cap.read()

    # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # out = cv2.VideoWriter('output.mp4', fourcc, image.get(cv2.CAP_PROP_FPS), (image.shape[1], image.shape[0]))

    h, w = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, scalefactor=1., size=(300, 300), mean=(104., 177., 123.))
    facenet.setInput(blob)
    dets = facenet.forward()
    
    while(True):

        for i in range(dets.shape[2]):
            confidence = dets[0, 0, i, 2]
            if confidence < 0.5:
                continue

            x1 = int(dets[0, 0, i, 3] * w)
            y1 = int(dets[0, 0, i, 4] * h)
            x2 = int(dets[0, 0, i, 5] * w)
            y2 = int(dets[0, 0, i, 6] * h)

            face = image[y1:y2, x1:x2]
            try:
                face_input = cv2.resize(face, dsize=(224, 224))
                face_input = cv2.cvtColor(face_input, cv2.COLOR_BGR2RGB)
                face_input = preprocess_input(face_input)
                face_input = np.expand_dims(face_input, axis=0)
            except Exception as e:
                # print(str(e))
                pass
            mask, nomask = model.predict(face_input).squeeze()

            if mask > nomask:
                color = (0, 255, 0)
                label = 'Mask %d%%' % (mask * 100)
            else:
                color = (0, 0, 255)
                label = 'No Mask %d%%' % (nomask * 100)
                messagebox.showwarning("<경고>","마스크 미착용자가 발견되었습니다.")

            cv2.rectangle(image, pt1=(x1, y1), 
                        pt2=(x2, y2),thickness=2, 
                        color=color, 
                        lineType=cv2.LINE_AA)
            cv2.putText(image, text=label, 
                        org=(x1, y1 - 10), 
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.8, color=color, 
                        thickness=2, lineType=cv2.LINE_AA)

            if label == 'No Mask':
                print("No MASK")

        return image

