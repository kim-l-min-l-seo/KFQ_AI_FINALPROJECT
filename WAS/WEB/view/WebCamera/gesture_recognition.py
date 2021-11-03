import tensorflow as tf
tf.debugging.set_log_device_placement(True)
from tensorflow.keras.models import load_model
import cv2
import mediapipe as mp
import numpy as np
import os
import requests
import json


def gesture_recognition(img):
    URL = "http://121.128.137.4:5000/keydown"
    seq = []
    action_seq = []
    actions = ['up', 'left', 'right', 'down']
    seq_length = 30
    file_path = os.path.join(os.getcwd()+"\WEB\\"+"view\\", "WebCamera\models\ytest.h5")
    model = load_model(file_path)
    # MediaPipe hands model
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    # image = cv2.VideoCapture(0)
    # w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # out = cv2.VideoWriter('input.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))
    # out2 = cv2.VideoWriter('output.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))
    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    while(True):
        if img is not None:
            result = hands.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # 영상에 hand landmark가 찍힐 때 아래 로직 수행
        if result.multi_hand_landmarks is not None:
            for res in result.multi_hand_landmarks:
                joint = np.zeros((21, 4))
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z, lm.visibility]
                # Compute angles between joints
                v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11,
                            0, 13, 14, 15, 0, 17, 18, 19], :3]  # Parent joint
                v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                            13, 14, 15, 16, 17, 18, 19, 20], :3]  # Child joint
                v = v2 - v1  # [20, 3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
                # Get angle using arcos of dot product
                angle = np.arccos(np.einsum('nt,nt->n',
                                            v[[0, 1, 2, 4, 5, 6, 8, 9, 10,12, 13, 14, 16, 17, 18], :],
                                            v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]
                angle = np.degrees(angle)  # Convert radian to degree
                d = np.concatenate([joint.flatten(), angle])
                seq.append(d)
                mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
                if len(seq) < seq_length:
                    continue
                input_data = np.expand_dims(
                    np.array(seq[-seq_length:], dtype=np.float32), axis=0)
                y_pred = model.predict(input_data).squeeze()
                i_pred = int(np.argmax(y_pred))
                conf = y_pred[i_pred]
                if conf < 0.9:
                    continue
                action = actions[i_pred]
                action_seq.append(action)
                if len(action_seq) < 3:
                    continue
                this_action = '?'
                if action_seq[-1] == action_seq[-2] == action_seq[-3]:
                    this_action = action
                print("action : ", action)
                # if action == "up":
                #     print(" 위 ")
                #     data = {
                #         'keyCode': 87,
                #         'hasShift': 0,
                #         'hasCtrl': 0,
                #         'hasAlt': 0
                #     }
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                    
                # elif action == "left":
                #     print(" 왼쪽 ")
                #     data = {
                #         'keyCode': 65,
                #         'hasShift': 0,
                #         'hasCtrl': 0,
                #         'hasAlt': 0
                #     }
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                # elif action == "right":
                #     print(" 오른쪽 ")
                #     data = {
                #         'keyCode': 68,
                #         'hasShift': 0,
                #         'hasCtrl': 0,
                #         'hasAlt': 0
                #     }
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                # elif action == "down":
                #     print(" 아래 ")
                #     data = {
                #         'keyCode': 83,
                #         'hasShift': 0,
                #         'hasCtrl': 0,
                #         'hasAlt': 0
                #     }
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                #     requests.post(URL, data=json.dumps(data))
                cv2.putText(img, f'{this_action.upper()}',
                            org=(int(
                                res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0] + 20)),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1,
                            color=(255, 255, 255),
                            thickness=2
                            )
        return img
