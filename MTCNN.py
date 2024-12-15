import cv2 
import numpy as np
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import pickle
from keras_facenet import FaceNet
import gpiozero
from gpiozero import DistanceSensor

facenet = FaceNet()
faces_embeddings = np.load('faces_detect_emb.npz')
Y = faces_embeddings['arr_1']
encoder = LabelEncoder()
encoder.fit(Y)
haarcascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = pickle.load(open('svm_face_model.pkl', 'rb'))

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()
    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haarcascade.detectMultiScale(gray_img, 1.3, 5)
    for x, y, w, h in faces:
        img = rgb_img[y:y+h, x:x+w]
        img = cv2.resize(img, (160, 160))
        img = np.expand_dims(img, axis=0)
        y_pred = facenet.embeddings(img)
        face_name = model.predict(y_pred)
        final_name = encoder.inverse_transform(face_name)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 10)
        cv2.putText(frame, str(final_name), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
    
    cv2.imshow('Face Recognition', frame)
    # print("Frame:", frame)
    # print("Frame:", faces)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()