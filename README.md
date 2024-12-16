# Smart Home System with Face Detection, Ultrasonic Sensor, and Mobile App Control

This project combines a face detection and ultrasonic sensor-based automated door system with a Smart Home mobile application built using Android Studio. The mobile app communicates with Firebase to control LED lighting, enabling seamless interaction between hardware and software components.

Features

Hardware: ESP32 with Ultrasonic Sensor and Face Detection

	1.	Face Detection and Recognition:
	•	Detect faces using OpenCV.
	•	Recognize authorized users using a trained SVM model.
	2.	Ultrasonic Sensor:
	•	Detects the presence of a person or object within a specific range.
	•	Triggers the face detection process.
	3.	Door Automation:
	•	Opens or closes the door using a servo motor based on face recognition results.
	4.	Firebase Integration:
	•	Sends and retrieves real-time data, enabling communication with the Android app.

Software: Android Smart Home App

	1.	Mobile App Features:
	•	Control LED brightness (analog value) and on/off state (digital value).
	•	Communicate with Firebase Realtime Database to send commands to the ESP32.
	2.	Firebase Integration:
	•	Sends user input to the database for controlling connected hardware.
	•	Displays success/failure messages for user feedback.
	3.	Material Design:
	•	Provides an intuitive user interface for controlling home devices.

Hardware Setup

	1.	Components:
	•	ESP32 for processing and connectivity.
	•	HCSR04 Ultrasonic Sensor for proximity detection.
	•	Camera for face detection and recognition.
	•	Servo Motor for door automation.
	•	LED for demonstrating smart home control via the mobile app.
	2.	Connections:
	•	Connect ultrasonic sensor, servo motor, and LED to the ESP32.
	•	Ensure ESP32 communicates with Firebase.
	3.	Firebase Realtime Database Structure:

LED/
   digital: <boolean>  // LED on/off
   analog: <integer>   // LED brightness

Mobile App Setup

	1.	Dependencies:
Add the following to your build.gradle file:

implementation 'com.google.firebase:firebase-database:20.0.5'
implementation 'androidx.activity:activity-ktx:1.7.2'


	2.	App Functionality:
	•	Button toggles LED brightness (analog) and state (digital).
	•	Sends the values to Firebase for the ESP32 to process.
	3.	Activity Code:

package com.example.homekit

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.homekit.databinding.ActivityMainBinding
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private lateinit var database: DatabaseReference
    private var isLightOn = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.buttonRead.setOnClickListener {
            toggleLight()
        }
    }

    private fun toggleLight() {
        isLightOn = !isLightOn
        val analogValue = if (isLightOn) 255 else 0
        val digitalValue = isLightOn

        controlLED(analogValue, digitalValue)
    }

    private fun controlLED(analogValue: Int, digitalValue: Boolean) {
        database = FirebaseDatabase.getInstance().reference
        val analogRef = database.child("LED").child("analog")
        analogRef.setValue(analogValue)
            .addOnSuccessListener {
                Toast.makeText(this, "Analog value set successfully", Toast.LENGTH_SHORT).show()
            }
            .addOnFailureListener {
                Toast.makeText(this, "Failed to set analog value", Toast.LENGTH_SHORT).show()
            }

        val digitalRef = database.child("LED").child("digital")
        digitalRef.setValue(digitalValue)
            .addOnSuccessListener {
                Toast.makeText(this, "Digital value set successfully", Toast.LENGTH_SHORT).show()
            }
            .addOnFailureListener {
                Toast.makeText(this, "Failed to set digital value", Toast.LENGTH_SHORT).show()
            }
    }
}

Integration Workflow

	1.	Hardware-Software Communication:
	•	The Android app sends analog and digital values to Firebase.
	•	The ESP32 retrieves these values and adjusts the LED’s state and brightness.
	2.	Real-time Updates:
	•	Firebase ensures real-time synchronization between the app and ESP32.
	•	Allows instant control and feedback.
	3.	Face Recognition:
	•	If the ultrasonic sensor detects a person, the ESP32 triggers the face recognition process.
	•	Authorizes entry by controlling the servo motor and updating Firebase.
