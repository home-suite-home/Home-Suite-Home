// user configurable settings
#include "config.h"

// NodeMCU V12E Libraries 
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// SSID and Password of your WiFi router
const char* ssid = NETWORK_NAME;
const char* password = NETWORK_PASSWORD;

// cs811 CO2 and TVOC Sensor
#include "Adafruit_CCS811.h"
Adafruit_CCS811 ccs;

// Declare a global object variable from the ESP8266WebServer class
ESP8266WebServer server(80); //Server on port 80 - Standard for HTTP


void setup() 
{
  Serial.begin(57600);

  // start cs811
  ccs.begin();
  Serial.println("CCS811 Init");

  if(!ccs.begin()){
    Serial.println("Failed to start sensor! Please check your wiring.");
  }

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
  server.on("/co2", handleCO2);
  server.on("/tvoc", handleTVOC);

  // Open the server for requests
    server.begin();
    Serial.println("HTTP server started");

}

void loop() 
{
    server.handleClient();
}


void handleCO2()
{
    String sensorValue = String(getCO2());
    Serial.print("CO2 value retrieved: ");
    Serial.println(sensorValue);
    server.send(200, "text/html", sensorValue);
}

double getCO2()
{   
    ccs.readData(); // must read available data before returning new value
    return ccs.geteCO2();
}


void handleTVOC()
{
    String sensorValue = String(get_TVOC());
    Serial.print("TVOC value retrieved: ");
    Serial.println(sensorValue);
    server.send(200, "text/html", sensorValue);
}

double get_TVOC()
{   
    ccs.readData(); // must read available data before returning new value
    return ccs.getTVOC();
}


// This page will display if the ip address is accessed with no HTTP plug 
void handleRoot() 
{
   Serial.println("Root page reached");
   String s = "rootPage\n";
   server.send(200, "text/html", s); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}