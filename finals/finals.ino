#include <Arduino.h>
#include <WiFi.h>               //we are using the ESP32
//#include <ESP8266WiFi.h>      // uncomment this line if you are using esp8266 and comment the line above
#include <Firebase_ESP_Client.h>

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
#define WIFI_SSID "X11L5NE"
#define WIFI_PASSWORD "Concentration"

// Insert Firebase project API Key
#define API_KEY "AIzaSyB7ofyN_Xo0zdrwMnd7yVpnnnQ5guBEvcU"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://smart-home-a72e9-default-rtdb.asia-southeast1.firebasedatabase.app/" 

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
int count = 0;
bool signupOK = false;                     //since we are doing an anonymous sign in 
const int ledPin = 2; // GPIO 2 on ESP32

void setup(){
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}


void loop() {
  // Check if Firebase is ready
  if (Firebase.ready() && signupOK) {
    // Read digital LED status from Firebase
    if (Firebase.RTDB.getBool(&fbdo, "/LED/digital")) {
      if (fbdo.dataType() == "boolean") {
        bool ledStatus = fbdo.boolData();
        Serial.println("Read digital LED status: " + String(ledStatus));
        digitalWrite(ledPin, ledStatus ? HIGH : LOW);
      }
    } else {
      Serial.println("Failed to read digital LED status: " + fbdo.errorReason());
    }

    // Read analog LED value from Firebase
    if (Firebase.RTDB.getInt(&fbdo, "/LED/analog")) {
      if (fbdo.dataType() == "int") {
        int pwmValue = fbdo.intData();
        Serial.println("Read analog LED value: " + String(pwmValue));
        analogWrite(ledPin, pwmValue);
      }
    } else {
      Serial.println("Failed to read analog LED value: " + fbdo.errorReason());
    }
  }

  // Add delay or other operations here if needed
}
