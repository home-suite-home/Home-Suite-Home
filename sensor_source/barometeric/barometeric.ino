// user configurable settings
#include "config.h"

// NodeMCU V12E Libraries 
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// SSID and Password of your WiFi router
const char* ssid = NETWORK_NAME;
const char* password = NETWORK_PASSWORD;


// Declare a global object variable from the ESP8266WebServer class
ESP8266WebServer server(80); //Server on port 80 - Standard for HTTP


#include "Wire.h"
#include "Adafruit_BMP085.h"
#include <math.h>

Adafruit_BMP085 bmp;

void setup() 
{
  Serial.begin(57600);

  bmp.begin();

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

  server.on("/", handleRoot); // handle if the root address is accessed - this is an error
  server.on("/temperature", handleTemperature);
  server.on("/pressure", handlePressure);
  server.on("/altitude", handleAltitude);

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
    String sensorValue = String(getTemperature());
    Serial.print("Temperature retrieved: ");
    Serial.println(sensorValue);
    server.send(200, "text/html", sensorValue);
}

double getTemperature()
{   
    double sensorValue = bmp.readTemperature();
    
    return sensorValue;
}


void handlePressure()
{
    String sensorValue = String(getPressure());
    Serial.print("Pressure retrieved: ");
    Serial.println(sensorValue);
    server.send(200, "text/html", sensorValue);
}

double getPressure()
{   
    int sensorValue = bmp.readPressure();
    
    return sensorValue;
}


void handleAltitude()
{
    String sensorValue = String(getAltitude());
    Serial.print("Altitude retrieved: ");
    Serial.println(sensorValue);
    server.send(200, "text/html", sensorValue);
}

double getAltitude()
{
    double altitude = ((pow((101325.0/getPressure()), (1/5.257)) - 1) * (getTemperature() + 273.15))/0.0065;

    return altitude;
}


// This page will display if the ip address is accessed with no HTTP plug 
void handleRoot() 
{
   Serial.println("Root page reached");
   String s = "rootPage\n";
   server.send(200, "text/html", s); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}