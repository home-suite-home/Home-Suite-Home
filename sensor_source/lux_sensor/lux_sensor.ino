// Math for calculating Lux: https://jxxcarlson.medium.com/measuring-light-intensity-with-arduino-a575765c0862

// NodeMCU V12E Libraries 
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// wifi username and password
#include "creds.h"

#include <math.h>

#define REF_VOLTS 3.3
#define VOLTS_CONSTANT 0.003222656 // 3.3 / 1024

#define sensorPin A0

// SSID and Password of your WiFi router
const char* ssid = NETWORK_NAME;
const char* password = NETWORK_PASSWORD;

ESP8266WebServer server(80); //Server on port 80 - Standard for HTTP

const double k = 3.3 / 1024.0;
const double luxFactor = 500000;
const double R2 = 10000;
const double B = 1.3 * pow(10.0, 7);
const double m = -1.4;


void setup() {
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

    // add HTTP plugs and the functions that support the command
    server.on("/", handleRoot); // handle if the root address is accessed - this is an error
    server.on("/lux", handleLux); // handle a request for sensor data

    // Open the server for requests
    server.begin();
    Serial.println("HTTP server started");
}

void loop() 
{
    server.handleClient();
}


void handleLux()
{
    Serial.println("Lux Requested.");
    String lux = String(getLux());
    Serial.print("Lux: ");
    Serial.println(lux);
    server.send(200, "text/html", lux);
}


double getLux()
{
    double V2 = k * analogRead(sensorPin);
    double R1 = (REF_VOLTS / V2 - 1) * R2;
    double lux = B * pow(R1, m);
    return lux;
}


// This page will display if the ip address is accessed with no HTTP plug 
void handleRoot() 
{
   Serial.println("Root page reached");
   String s = "rootPage\n";
   server.send(200, "text/html", s); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}