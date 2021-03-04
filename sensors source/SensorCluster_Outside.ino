//
//  Filename: SensorCluster_Outside.ino
//  Date: 03/04/2021
//
//  Engineer: Wyatt Vining
//  Contact: wyatt.vining@knights.ucf.edu
//
//  Note: Enginnering asset - Not for production use 
//  
//  Hardware Configuration:
//    - DS18B20 Temperature Sensor x5
//    - SHT31 Temperature and Humidity Sensor x1
//    - DHT22 Temperature and Humidity Sensor x2
//
//  Description:
//    This is a cluster of sensors we are using for two purposes:
//      1. Hardware validation 
//      2. Standard database creation for those who do not have direct hardware access
// 



// DS18 Libraries
#include <OneWire.h>
#include <DallasTemperature.h>

// NodeMCU V12E Libraries 
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// SHT31 Sensor and I2C Libraries
#include <Wire.h>
#include "Adafruit_SHT31.h"

// DHT22 library
#include <DHT.h>

// DS18 Bus Pin
#define ONE_WIRE_BUS D6

// DHT22 constants
#define DHTTYPE DHT22
#define dhtpin1 D4
#define dhtpin2 D5

// DS18 Init
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS(&oneWire);

// DHT 22 init
DHT dht1(dhtpin1, DHTTYPE);
DHT dht2(dhtpin2, DHTTYPE);

// Declare a global object for temperature / humidity sensor
Adafruit_SHT31 sht31 = Adafruit_SHT31();

// SSID and Password of your WiFi router
const char* ssid = "NETWORK_NAME";
const char* password = "NETWORK_PASSWORD";

// Declare a global object variable from the ESP8266WebServer class
ESP8266WebServer server(80); //Server on port 80 - Standard for HTTP

// DS18 Addresses
uint8_t sensor1[8] = {0x28, 0x74, 0xB5, 0x07, 0xD6, 0x01, 0x3C, 0x50};
uint8_t sensor2[8] = {0x28, 0x66, 0xCE, 0x07, 0xD6, 0x01, 0x3C, 0x78};
uint8_t sensor3[8] = {0x28, 0x29, 0x50, 0x07, 0xD6, 0x01, 0x3C, 0x3C};
uint8_t sensor4[8] = {0x28, 0xCB, 0x97, 0x07, 0xD6, 0x01, 0x3C, 0x08};
uint8_t probe[8] = {0x28, 0x9F, 0xBA, 0x07, 0xD6, 0x01, 0x3C, 0xEE};

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

    // add HTTP plugs and the functions that support the command
    server.on("/", handleRoot); // handle if the root address is accessed - this is an error
    server.on("/temperatureSHT", handleTemperatureSHT); // handle a request for sensor data
    server.on("/humiditySHT", handleHumiditySHT); // handle a request for sensor data
    server.on("/sensor1", handleTemperatureSensor1);
    server.on("/sensor2", handleTemperatureSensor2);
    server.on("/sensor3", handleTemperatureSensor3);
    server.on("/sensor4", handleTemperatureSensor4);
    server.on("/probe", handleTemperatureProbe);
    server.on("/dht1temperature", handleTemperatureDHT1);
    server.on("/dht2temperature", handleTemperatureDHT2);
    server.on("/dht1humidity", handleHumidityDHT1);
    server.on("/dht2humidity", handleHumidityDHT2);

    // Open the server for requests
    server.begin();
    Serial.println("HTTP server started");

    // Start Temperature / Humidity Sensor 
    Serial.println("SHT31 test");
    
    if (! sht31.begin(0x44)) // Set to 0x45 for alternate i2c addr - Needed for two temp sensors 
    {   
        Serial.println("Couldn't find SHT31");
    }
    
    DS.begin();

    dht1.begin();
    dht2.begin();
}

void loop() 
{
    // handle a client request - direct the clients to the page they request using server.on() above
    server.handleClient(); 

}


// This page will display if the ip address is accessed with no HTTP plug 
void handleRoot() 
{
   Serial.println("Root page reached");
   String s = "rootPage\n";
   server.send(200, "text/html", s); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}


void handleTemperatureDHT1()
{
    String tempC = String(dht1.readTemperature(false), 2);
    Serial.print("DHT22 sensor 1 temp C: ");
    Serial.println(tempC);
    server.send(200, "text/html", tempC);
}


void handleTemperatureDHT2()
{
    String tempC = String(dht2.readTemperature(false), 2);
    Serial.print("DHT22 sensor 2 temp C: ");
    Serial.println(tempC);
    server.send(200, "text/html", tempC);
}


void handleHumidityDHT1()
{
    String humidity = String(dht1.readHumidity(), 2);
    Serial.print("DHT22 sensor 1 humidity: ");
    Serial.println(humidity);
    server.send(200, "text/html", humidity);
}


void handleHumidityDHT2()
{
    String humidity = String(dht2.readHumidity(), 2);
    Serial.print("DHT22 sensor 2 humidity: ");
    Serial.println(humidity);
    server.send(200, "text/html", humidity);
}


// this page will be reached if the HTTP plug is "/temperature"
void handleTemperatureSHT() 
{ 
     Serial.println("Temperature request recieved");
     String temp = String(getTemp());
     server.send(200, "text/html", temp); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
}


void handleTemperatureSensor1()
{
    DS.requestTemperatures();
    double tempC = (double)DS.getTempC(sensor1);
    Serial.print("DS Sensor 1: ");
    Serial.println(tempC);
    String celcius = String(tempC);
    server.send(200, "text/html", celcius);
}

void handleTemperatureSensor2()
{
    DS.requestTemperatures();
    double tempC = (double)DS.getTempC(sensor2);
    Serial.print("DS Sensor 2: ");
    Serial.println(tempC);
    String celcius = String(tempC);
    server.send(200, "text/html", celcius);
}


void handleTemperatureSensor3()
{
    DS.requestTemperatures();
    double tempC = (double)DS.getTempC(sensor3);
    Serial.print("DS Sensor 3: ");
    Serial.println(tempC);
    String celcius = String(tempC);
    server.send(200, "text/html", celcius);
}


void handleTemperatureSensor4()
{
    DS.requestTemperatures();
    double tempC = (double)DS.getTempC(sensor4);
    Serial.print("DS Sensor 4: ");
    Serial.println(tempC);
    String celcius = String(tempC);
    server.send(200, "text/html", celcius);
}


void handleTemperatureProbe()
{
    DS.requestTemperatures();
    double tempC = (double)DS.getTempC(probe);
    Serial.print("DS Sensor probe: ");
    Serial.println(tempC);
    String celcius = String(tempC);
    server.send(200, "text/html", celcius);
}


// this page will be reached if the HTTP plug is "/humidity"
void handleHumiditySHT()
{
    Serial.println("Humidity Request Recieved");
    double humidity = (double)sht31.readHumidity();
    String humidityStr = String(humidity, 2);
    server.send(200, "text/html", humidityStr); // server.send(RESPONSE(should be 200), TYPE(Arbitrary data type), STRING(to be sent))
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
    double humidity = (double)sht31.readHumidity(); // float is the default - cast as an int since the accuracy for the sensor is only out to the tens deciamal anyway

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
