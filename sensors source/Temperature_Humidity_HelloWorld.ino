//
//  Date: 02/09/2021
//  FileName: Temperature_Humidity_HelloWorld.ino
//  
//  Engineer: Wyatt Vining
//  Contact: wyatt.vining@knights.ucf.edu
//
//  Description: 
//    This is a basic implementation of an SHT31-D temperature and humidity sensor running on a NodeMCU 12E Arduino.
//    The purpose of this sketch is to demonstrate a network connected arduino capable of returning sensor values to client requests.
//    This will act as a framework for all sensors within the scope of this project and with that has verbose comments.
//
//  Assets:
//    1. NodeMCU board manager: https://arduino.esp8266.com/stable/package_esp8266com_index.json
//    2. ESP8266 header files: included with board install
//    3. Adafruit_SHT31.h: https://github.com/adafruit/Adafruit_SHT31
//

// NodeMCU V12E Libraries 
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// Temperature Sensor and I2C Libraries
#include <Wire.h>
#include "Adafruit_SHT31.h"

// Declare a global object for temperature / humidity sensor
Adafruit_SHT31 sht31 = Adafruit_SHT31();

// SSID and Password of your WiFi router
const char* ssid = "Wi-Fi Network";
const char* password = "3212580352";

// Declare a global object variable from the ESP8266WebServer class
ESP8266WebServer server(80); //Server on port 80 - Standard for HTTP


// This is the setup code that is executed once when the arduino is turned on
void setup() 
{
    // Initialize the serial connection - USB 
    // Serial.begin(BAUD_RATE)
    Serial.begin(57600); 

    WiFi.begin(ssid, password);     //Connect to your WiFi router
    Serial.println("");

    // loop until connection successful
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(500);
        Serial.print(".");
    }

    //If connection successful show IP address in serial monitor
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());  //IP address assigned to your ESP

    // add HTTP plugs and the functions that support the command
    server.on("/", handleRoot); // handle if the root address is accessed - this is an error
    server.on("/temperature", handleTemperature); // handle a request for sensor data
    server.on("/humidity", handleHumidity); // handle a request for sensor data

    // Open the server for requests
    server.begin();
    Serial.println("HTTP server started");

    // Start Temperature / Humidity Sensor 
    Serial.println("SHT31 test");
    
    if (! sht31.begin(0x44)) // Set to 0x45 for alternate i2c addr - Needed for two temp sensors 
    {   
        Serial.println("Couldn't find SHT31");
    }
}


// This code will loop as long as the arduino is on
void loop() 
{
    // handle a client request
    server.handleClient(); 
}


// This page will display if the ip address is accessed with no HTTP plug 
void handleRoot() 
{
   Serial.println("Root page reached");
   String s = "rootPage\n";
   server.send(200, "text/html", s); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}


// this page will be reached if the HTTP plug is "/temperature"
void handleTemperature() 
{ 
     Serial.println("Temperature request recieved");
     String temp = String(getTemp());
     server.send(200, "text/html", temp); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}


// this page will be reached if the HTTP plug is "/humidity"
void handleHumidity()
{
    Serial.println("Humidity Request Recieved");
    String humidity = String(getHumidity());
    server.send(200, "text/html", humidity); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
} 


// returns the current temperature in degrees celcius
double getTemp()
{
    // get the temperature from the sensor
    double temperature = (double)sht31.readTemperature(); // The default value is a float - we cast as a double for efficiency

    // check if the temperature was read properly - this is unnecessary for the sensor but useful for debugging 
    if (! isnan(temperature))
    {
        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.println("C");
    }
    else
    {
        Serial.println("Failed to read temperature");
    }

    return temperature; // will return nan if there is an issue with the sensor
}


// returns the current relative humidity percentage
int getHumidity()
{
    // get the relative humidity from the sensor 
    int humidity = (int)sht31.readHumidity(); // float is the default - cast as an int since the accuracy for the sensor is only out to the tens deciamal anyway

    // check if humidity was read from the sensor properly
    if (! isnan(humidity))
    {
        Serial.print("Humidity: ");
        Serial.print(humidity);
        Serial.println("%");
    }
    else
    {
        Serial.println("Failed to read temperature");
    }

    return humidity; // will return nan if there is an issue with the sensor
}
