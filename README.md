# Face Detection and Ultrasonic Sensor-Based Door Control System

This project integrates face detection and recognition with an ultrasonic sensor to create an automated door control system. The system uses a camera for face detection, a machine learning model for recognition, an ultrasonic sensor for proximity detection, and a servo motor to control door movement.

Features

	1.	Face Detection and Recognition:
	•	Detects faces using OpenCV’s Haar Cascade Classifier.
	•	Recognizes detected faces using pre-trained embeddings and an SVM classifier.
	2.	Ultrasonic Sensor:
	•	Measures distance to detect the presence of a person or object.
	•	Triggers face recognition if a person is within 150 cm.
	3.	Door Automation:
	•	Controls a servo motor to open or close a door based on face recognition results.
	•	Allows authorized users (based on the face recognition model) to open the door.
	4.	LCD Integration:
	•	Provides visual feedback to users.
	•	Displays messages like “Please Identify,” “Identify Success,” or “Access Denied.”
	5.	Safety Features:
	•	Graceful termination of the program using signal handling.
	•	GPIO cleanup ensures hardware safety after the program ends.

Components Used

	1.	Hardware:
	•	Ultrasonic Sensor: HCSR04 module for proximity detection.
	•	Servo Motor: Controls door movement.
	•	Camera: Captures live video for face recognition.
	•	LCD Screen: Displays status and feedback messages.
	2.	Software and Libraries:
	•	cv2 (OpenCV): For face detection and real-time video processing.
	•	FaceNet (Keras): Generates face embeddings for recognition.
	•	gpiozero & RPi.GPIO: For controlling GPIO pins on Raspberry Pi.
	•	HCSR04: Custom library for ultrasonic sensor integration.
	•	rpi_lcd: For interfacing with the LCD.
	•	pickle: Loads the pre-trained SVM model for recognition.
	•	tensorflow, numpy, sklearn: Supporting machine learning and preprocessing.

How It Works

	1.	Ultrasonic Sensor Detection:
	•	Measures the distance of nearby objects.
	•	If a person is within 150 cm, the system initiates face detection.
	2.	Face Detection:
	•	Captures a video frame using the camera.
	•	Detects faces in the frame using the Haar Cascade Classifier.
	3.	Face Recognition:
	•	Extracts face embeddings using the FaceNet model.
	•	Classifies the detected face using a pre-trained SVM model.
	•	Matches the face against authorized users.
	4.	Door Control:
	•	If the detected face matches an authorized user, the servo motor opens the door.
	•	If unauthorized, the system displays “Access Denied” on the LCD.
	5.	Feedback:
	•	Status and results are displayed on the LCD.
	•	The servo motor operates based on recognition results.

Setup Instructions

	1.	Hardware Connections:
	•	Connect the HCSR04 ultrasonic sensor to GPIO pins 5 (Echo) and 6 (Trig).
	•	Connect the servo motor to GPIO pin 23.
	•	Connect the LCD to the appropriate I2C pins on the Raspberry Pi.
	2.	Pre-trained Model:
	•	Place faces_detect_emb.npz and svm_face_model.pkl in the working directory.
	•	Ensure the Haar Cascade XML file (haarcascade_frontalface_default.xml) is in the same directory.
	3.	Install Required Libraries:

pip install opencv-python keras-facenet tensorflow rpi_lcd gpiozero

  4.	Testing:
	•	Stand within 150 cm of the ultrasonic sensor.
	•	Look at the camera for face recognition.
	•	Observe the LCD messages and servo motor behavior.

Troubleshooting

	1.	Camera Not Working:
	•	Ensure the camera is connected and enabled in Raspberry Pi settings.
	2.	Servo Motor Issues:
	•	Check GPIO connections and power supply to the motor.
	3.	Recognition Accuracy:
	•	Retrain the SVM model with more diverse face images if recognition fails.
	4.	Ultrasonic Sensor:
	•	Verify correct GPIO pin setup if the sensor does not detect proximity.

Future Enhancements

	•	Add a buzzer for failed recognition attempts.
	•	Integrate a database for logging entry attempts.
	•	Support multiple ultrasonic sensors for improved range detection.
