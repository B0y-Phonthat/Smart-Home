#ESP32 Firebase LED Control

This project demonstrates how to use an ESP32 microcontroller to interact with a Firebase Realtime Database (RTDB) to control an LED. The project includes reading digital and analog values from Firebase to control the LED’s state and brightness.

Features

	•	Wi-Fi Connection: Connects the ESP32 to a specified Wi-Fi network.
	•	Firebase Integration: Authenticates with Firebase using an anonymous sign-in and communicates with the RTDB.
	•	LED Control:
	•	Reads a boolean value from Firebase to turn the LED ON or OFF.
	•	Reads an integer value from Firebase to set the LED brightness using PWM (analog control).

Setup Instructions

	1.	Hardware Requirements:
	•	ESP32 board.
	•	An LED connected to GPIO 2 (built-in LED or external).
	2.	Software Requirements:
	•	Arduino IDE with the following libraries installed:
	•	Firebase ESP Client for Firebase integration.
	•	WiFi for Wi-Fi communication.
	3.	Configuration:
	•	Replace the placeholders in the code with your details:

#define WIFI_SSID "YOUR_WIFI"       // Your Wi-Fi SSID
#define WIFI_PASSWORD "YOUR_PASSWD" // Your Wi-Fi password
#define API_KEY "FIREBASE_API"      // Firebase project API key
#define DATABASE_URL "Firebase_URL" // Firebase Realtime Database URL


	4.	Compile and Upload:
	•	Compile the sketch and upload it to the ESP32 using the Arduino IDE.
	•	Open the Serial Monitor to verify the connection and debug information.

How It Works

	1.	Initialization:
	•	Connects to Wi-Fi.
	•	Sets up Firebase using the provided API key and database URL.
	•	Performs an anonymous sign-in to Firebase.
	2.	Real-time Database Interaction:
	•	Monitors /LED/digital in Firebase for a boolean value:
	•	true: Turns the LED ON.
	•	false: Turns the LED OFF.
	•	Monitors /LED/analog in Firebase for an integer value:
	•	Updates the LED brightness via PWM.
	3.	Feedback:
	•	Outputs the current status of the LED (digital and analog) to the Serial Monitor.
	•	Displays error messages if reading from Firebase fails.

File Structure

	•	Main Code:
	•	Handles Wi-Fi connection, Firebase setup, and data processing.
	•	Add-ons:
	•	TokenHelper.h: Handles token generation and status callbacks.
	•	RTDBHelper.h: Includes helper functions for database interactions.

Notes

	•	Ensure your Firebase project has a Realtime Database enabled.
	•	Use the Firebase Console to update /LED/digital and /LED/analog values for testing.
	•	For ESP8266, uncomment the corresponding #include <ESP8266WiFi.h> line and comment out the ESP32-specific line.
