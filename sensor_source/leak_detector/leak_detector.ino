// user configurable settings
#include "config.h"

// NodeMCU V12E Libraries
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#define levelPin A0

// SSID and Password of your WiFi router
const char* ssid = NETWORK_NAME;
const char* password = NETWORK_PASSWORD;


// Declare a global object variable from the ESP8266WebServer class
ESP8266WebServer server(80); //Server on port 80 - Standard for HTTP


void setup()
{
  Serial.begin(57600);
  pinMode(levelPin, INPUT);

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
  server.on("/status", handleStatus);

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
    String sensorValue = String(getAvgValue());
    Serial.print("Sensor value retrieved: ");
    Serial.println(sensorValue);
    server.send(200, "text/html", sensorValue);
}

double getAvgValue()
{
    int averageValue = 0;
    int loops = 5;

    for (int i = 0; i < loops; i++)
    {
        int rawLevel = analogRead(levelPin);

        averageValue += rawLevel;

        delay(3);
    }

    averageValue /= loops;

    return averageValue;
}


// This page will display if the ip address is accessed with no HTTP plug
void handleRoot()
{
   Serial.println("Root page reached");
   String s = "rootPage\n";
   server.send(200, "text/html", s); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}
