// user configurable settings
#include "config.h"

// NodeMCU V12E Libraries 
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// SHT31 Sensor and I2C Libraries
#include <Wire.h>
#include "Adafruit_SHT31.h"

// Declare a global object for temperature / humidity sensor
Adafruit_SHT31 sht31 = Adafruit_SHT31();

// SSID and Password of your WiFi router
const char* ssid = NETWORK_NAME;
const char* password = NETWORK_PASSWORD;


// Declare a global object variable from the ESP8266WebServer class
ESP8266WebServer server(80); //Server on port 80 - Standard for HTTP


void setup() 
{
  Serial.begin(57600);

  WiFi.begin(ssid, password);     //Connect to your WiFi router
  Serial.println("");

  // loop until connection successful
  while (WiFi.status() != WL_CONNECTED) 
  {
      delay(500); // wait half a second before retrying connection 
      Serial.print(".");
  }

  //If connection successful show IP address in serial monitor
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());  //IP address assigned to your ESP

    // Start Temperature / Humidity Sensor 
    Serial.println("SHT31 test");
    
    if (! sht31.begin(0x44)) // Set to 0x45 for alternate i2c addr - Needed for two temp sensors 
    {   
        Serial.println("Couldn't find SHT31");
    }

    server.on("/", handleRoot); // handle if the root address is accessed - this is an error
    server.on("/temperature", handleTemperature);
    server.on("/humidity", handleHumidity);

  // Open the server for requests
    server.begin();
    Serial.println("HTTP server started");
}


void loop() 
{
    server.handleClient();
}


void handleTemperature()
{
    String temperature = String(getTemperature());
    Serial.print("Temperature value retrieved: ");
    Serial.println(temperature);
    server.send(200, "text/html", temperature);
}

double getTemperature()
{   
    double temperature = (double)sht31.readTemperature();
    
    return temperature;
}


void handleHumidity()
{
    String humidity = String(getHumidity());
    Serial.print("Humidity value retrieved: ");
    Serial.println(humidity);
    server.send(200, "text/html", humidity);
}

double getHumidity()
{   
    double humidity = (double)sht31.readHumidity();
    
    return humidity;
}


// This page will display if the ip address is accessed with no HTTP plug 
void handleRoot() 
{
   Serial.println("Root page reached");
   String s = "rootPage\n";
   server.send(200, "text/html", s); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}