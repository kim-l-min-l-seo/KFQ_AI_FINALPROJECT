import cv2
import os
import numpy as np

def ssdNet(image) :
    CONF_VALUE = 0.8 # 20% 인정
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe(os.getcwd()+"\WEB\\"+"view\\"+"TurtlebotCamera\models\MobileNetSSD_deploy.prototxt.txt",
                                   os.getcwd()+"\WEB\\"+"view\\"+"TurtlebotCamera\models\MobileNetSSD_deploy.caffemodel")
    # print(type(image), image)
    (h, w) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    count = 0
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONF_VALUE:
            count +=1
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            # print('count',count,label,CLASSES[idx])
            if CLASSES[idx] == "person" :
                # print('전방에 사람 발견\n 안전운행 요망',COLORS[idx])
                continue

            cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    return image
