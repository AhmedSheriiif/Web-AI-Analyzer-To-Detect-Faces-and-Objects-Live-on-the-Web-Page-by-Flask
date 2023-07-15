import os

from tensorflow.keras.utils import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt


class EmotionDetectorClass:
    EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
                "neutral"]

    def __init__(self, detection_model_path, emotion_model_path, detected_img_path=None):
        self.detection_model_path = detection_model_path
        self.emotion_model_path = emotion_model_path
        self.detected_img_path = detected_img_path

    def Load_Model(self):
        self.detection_model = cv2.CascadeClassifier(self.detection_model_path)
        self.emotion_model = load_model(self.emotion_model_path, compile=False)

    def infer_frame(self, frame):
        Detections = []
        frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detection_model.detectMultiScale(gray, scaleFactor=1.1,
                                                      minNeighbors=5, minSize=(30, 30),
                                                      flags=cv2.CASCADE_SCALE_IMAGE)

        canvas = np.zeros((250, 300, 3), dtype="uint8")
        frameClone = frame.copy()

        if len(faces) > 0:
            faces = sorted(faces, reverse=True,
                           key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (X, Y, W, H) = faces

            facial = gray[Y:Y + H, X:X + W]
            facial = cv2.resize(facial, (64, 64))
            facial = facial.astype("float") / 255.0
            facial = img_to_array(facial)
            facial = np.expand_dims(facial, axis=0)

            preds = self.emotion_model.predict(facial)[0]
            emotion_probability = np.max(preds)
            label = EmotionDetectorClass.EMOTIONS[preds.argmax()]
            Detections.append(label)

            for (i, (emotion, prob)) in enumerate(zip(EmotionDetectorClass.EMOTIONS, preds)):
                # construct the label text
                text = "{}: {:.2f}% ".format(emotion, prob * 100)
                w = int(prob * 300)
                cv2.putText(frameClone, label, (X, Y - 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 255), 2)
                cv2.rectangle(frameClone, (X, Y), (X + W, Y + H), (255, 0, 0), 2)

        return frameClone, Detections

    def Run_Detect(self, source=None, saving_name=None):
        if source is not None:
            img = cv2.imread(source)
            img_pred, Detections = self.infer_frame(img)
            saving_location = self.detected_img_path + "/" + saving_name
            print(saving_location)
            cv2.imwrite(saving_location, img_pred)
            return img_pred, Detections


