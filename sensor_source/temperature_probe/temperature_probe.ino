// user configurable settings
#include "config.h"

// NodeMCU V12E Libraries 
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// DS18 Libraries
#include <OneWire.h>
#include <DallasTemperature.h>

// DS18 Bus Pin
#define ONE_WIRE_BUS D2

// DS18 Init
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS(&oneWire);
DeviceAddress address;

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

    // start DS18B20 temperature sensors
    DS.begin();

    // locate devices on the bus
    Serial.print("Locating devices...");
    Serial.print("Found ");
    Serial.print(DS.getDeviceCount(), DEC);
    Serial.println(" devices.");

    // look up address of DS18
    if (!DS.getAddress(address, 0))
    {
        Serial.println("unable to locate device address");
    }

    // Set the max resolution for the DS18 sensor of 12 bits
    DS.setResolution(address, 12);

    server.on("/", handleRoot); // handle if the root address is accessed - this is an error
    server.on("/temperature", handleStatus);

  // Open the server for requests
    server.begin();
    Serial.println("HTTP server started");

}

void loop() 
{
    server.handleClient();
}


void handleStatus()
{
    String sensorValue = String(getTemperature());
    Serial.print("Temperature value retrieved: ");
    Serial.println(sensorValue);
    server.send(200, "text/html", sensorValue);
}

double getTemperature()
{   
    DS.requestTemperatures();
    
    double sensorValue = (double)DS.getTempCByIndex(0);
    
    return sensorValue;
}


// This page will display if the ip address is accessed with no HTTP plug 
void handleRoot() 
{
   Serial.println("Root page reached");
   String s = "rootPage\n";
   server.send(200, "text/html", s); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}