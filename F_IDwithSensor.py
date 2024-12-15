# IMPORT LIBRARIES
import cv2
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import pickle
from keras_facenet import FaceNet
import gpiozero
from gpiozero import DistanceSensor
import RPi.GPIO as GPIO
from time import sleep
from signal import signal, SIGTERM, SIGHUP
from threading import Thread
from rpi_lcd import LCD
import HCSR04 as HCSR04
import time

# SETUP PIN
# ----- Ultrasonic ---------
Echo = 5
Trig = 6
timeout = 0.5
sensor = HCSR04.HCSR04(Trig, Echo, timeout)
time.sleep(1)
running = True

# ----- Buzzer ---------
# buzzer_pin = 17
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(buzzer_pin, GPIO.OUT)

# ----- LCD ---------
reading = True
message = ""
lcd = LCD()

# Function to handle termination signals
def safe_exit(signum, frame):
    exit(1)
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

# ----- Servo ---------
GPIO.setmode(GPIO.BCM) #BCM # This line is removed to prevent the ValueError
GPIO.setup(23, GPIO.OUT)
servo1 = GPIO.PWM(23, 50)


# Function
def open_door():
    print("Opening the door")
    servo1.start(0)  # Start PWM
    servo1.ChangeDutyCycle(7)  # Move to 90 degrees
    time.sleep(1)  # Wait for the door to open

# Function to close the door
def close_door():
    print("Closing the door")
    servo1.ChangeDutyCycle(2)  # Move to 0 degrees
    time.sleep(1)  # Wait for the door to close
    servo1.stop()  # Stop PWM

# Face detect
facenet = FaceNet()
faces_embeddings = np.load('faces_detect_emb.npz')
Y = faces_embeddings['arr_1']
encoder = LabelEncoder()
encoder.fit(Y)
haarcascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = pickle.load(open('svm_face_model.pkl', 'rb'))

# Capture video from the camera
cap = cv2.VideoCapture(0)
while running:
    try:
        # Ultrasonic detect
        distance = sensor.distance()
        print('Distance object is', distance, 'cm')
        time.sleep(1)
        if distance < 150:
            # Camera face detect
            if cap.isOpened():  # Check if the camera is opened
                # Display on LCD
                lcd.clear()
                lcd.text("Please", 1)
                lcd.text("Identify", 2)
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
        
        lcd.clear
        lcd.text("Identify", 1)
        lcd.text("Success", 2)
        print(str(final_name))
        open_door()
        time.sleep(2)
        servo1.stop()
        # Check person
        if str(final_name) == ['Phonthat'] or str(final_name) == ['Sorawit']:
            lcd.clear
            lcd.text("Identify", 1)
            lcd.text("Success", 2)
            time.sleep(2)
            open_door()
        else:
            lcd.clear
            lcd.text("Access", 1)
            lcd.text("Denied", 2)
            #GPIO.output(buzzer_pin, GPIO.HIGH)
            #time.sleep(0.5)  # Buzzer on for 1 second
            #GPIO.output(buzzer_pin, GPIO.LOW)
            #time.sleep(0.5)  # Buzzer off for 1 second

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        running = False
        GPIO.cleanup()
        sensor.clean()  # Clean up GPIO
    #finally:
        #lcd.clear()  # Clear LCD

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()