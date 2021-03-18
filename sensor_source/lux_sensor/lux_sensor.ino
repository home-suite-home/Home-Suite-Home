// NodeMCU V12E Libraries 
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#include <math.h>

#define REF_VOLTS 3.3
#define VOLTS_CONSTANT 0.003222656 // 3.3 / 1024

#define sensorPin A0

const double k = 3.3 / 1024.0;
const double luxFactor = 500000;
const double R2 = 10000;
const double B = 1.3 * pow(10.0, 7);
const double m = -1.4;

double getLux()
{
    double V2 = k * analogRead(sensorPin);
    double R1 = (REF_VOLTS / V2 - 1) * R2;
    double lux = B * pow(R1, m);
    return lux;
}

void setup() {
    Serial.begin(57600);

}

void loop() {
  Serial.println(getLux());
  delay(500);

}


// double getLux()
// {
//     int rawData = analogRead(sensorPin);

//     double resistorVolts = (double)rawData / MAX_ADC * REF_VOLTS;

//     double sensorVolts = REF_VOLTS - resistorVolts;

//     double sensorResistance = sensorVolts / resistorVolts * RESISTANCE;

//     double lux = LUX_CONSTANT * pow(sensorResistance, LUX_EXP);

//     return lux;

// }


// double getLux()
// {
//     double sensorVolts = analogRead(sensorPin) * VOLTS_CONSTANT;
//     double lux = 500.0 /  (10.0 * ((REF_VOLTS - sensorVolts) / sensorVolts));
//     return lux;
// }
