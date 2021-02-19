#
#   Date: 2/18/21
#   File Name: htmlReader_MK_2.py
#
#   Engineer: Wyatt Vining
#   Contact: wyatt.vining@knights.ucf.edu
#
#   Description:
#       This is an object oriented script to demonstrate a method to retrieve sensor data from an HTML source.
#
#   Note:
#       This file is not intended for production use.
#
#   TODO:
#       Need to add error handling for unexpected / no response from sensor server.
#
from urllib.request import urlopen
import math

METRIC = "mertric"
IMPERIAL = "imperial"

class Sensor:

    def __init__(self, units, address):
        self.units = units
        self.address = address

    def requestData(self):
        self.page = urlopen(self.address)
        rawBytes = self.page.read()
        return rawBytes.decode("utf-8")

    def getSensorValue(self):
        dataString = self.requestData()
        sensorValue = float(dataString)
        return sensorValue

    def getUnits(self):
        return self.units()


class TemperatureSensor(Sensor):

    def getSensorValue(self):
        dataString = self.requestData()
        degreesCelsius = round(float(dataString), 2)
        if self.units == METRIC:
            return degreesCelsius
        else:
            degreesFahrenheit = round(((degreesCelsius * 1.8) + 32.0), 2)
            return degreesFahrenheit

    def getDegreesCelcius(self):
        dataString = self.requestData()
        degreesCelsius = float(dataString)
        return degreesCelsius

    def getUnits(self):
        if self.units == IMPERIAL:
            return "Fahrenheit"
        else:
            return "Celsius"


class HumiditySensor(Sensor):

    def getSensorValue(self):
        dataString = self.requestData()
        relativeHumidity = float(dataString)
        return relativeHumidity

    def getDewPoint(self, degreesCelsius):
        relativeHumidity = self.getSensorValue()
        dewPointCelsius = (243.12 * (math.log(relativeHumidity / 100) + ((17.62 * degreesCelsius) / (243.12 + degreesCelsius)))) / (17.62 - (math.log(relativeHumidity/100) + ((17.62 * degreesCelsius)/(243.12 + degreesCelsius))))
        dewPointCelsius = round(dewPointCelsius, 2)
        if self.units == METRIC:
            return dewPointCelsius
        else:
            dewPointFahrenheit = (dewPointCelsius * 1.8) + 32.0
            dewPointFahrenheit = round(dewPointFahrenheit, 2)
            return dewPointFahrenheit

    def getUnits(self):
        if self.units == IMPERIAL:
            return "Fahrenheit"
        else:
            return "Celsius"


temperatureSensorOne = TemperatureSensor(IMPERIAL, "http://localhost:8080/temperature")
humiditySensorOne = HumiditySensor(IMPERIAL, "http://localhost:8080/humidity")

print("Temperature in degrees ", temperatureSensorOne.getUnits(), ": ", temperatureSensorOne.getSensorValue())

print("Relative Humidity: ", humiditySensorOne.getSensorValue())
print("Dew Point ", humiditySensorOne.getUnits(), ": ", humiditySensorOne.getDewPoint(temperatureSensorOne.getDegreesCelcius()))
