#
#   Date: 2/24/21
#   File Name: Sensors.py
#
#   Engineer: Wyatt Vining
#   Contact: wyatt.vining@knights.ucf.edu
#
#   Description:
#       This is a script intended to retrieve, parse and return data from network connected sensors.
#
#

from urllib.request import urlopen
import math

METRIC = "mertric"
IMPERIAL = "imperial"

class Sensor:

    def __init__(self, url_plug, units = METRIC, domain = 'localhost', port = '80'):
        self.units = units
        try:
            self.address = 'http://' + domain + ':' + port + '/' + url_plug
        except Exception as e:
            print(e)
            self.address = ''

        # print("address(sensor): " + self.address)

    def requestData(self):
        try:
            self.page = urlopen(self.address)
        except Exception as e:
            print(e)
            return "NaN"
        rawBytes = self.page.read()
        rawString = rawBytes.decode("utf-8")
        try:
            float(rawString)
        except Exception as e:
            print(e)
            return "NaN"
        return rawString

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

    def calculateDewPoint(self, relativeHumidity, degreesCelsius):
        dewPoint = (243.12 * (math.log(relativeHumidity / 100) + ((17.62 * degreesCelsius) / (243.12 + degreesCelsius)))) / (17.62 - (math.log(relativeHumidity/100) + ((17.62 * degreesCelsius)/(243.12 + degreesCelsius))))
        dewPoint = round(dewPoint, 2)
        return dewPoint

    def getDewPoint(self, degreesCelsius):
        relativeHumidity = self.getSensorValue()
        dewPointCelsius = self.calculateDewPoint(relativeHumidity, degreesCelsius)
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


def main():
    temperatureSensorOne = TemperatureSensor(
        "temperature",
        IMPERIAL,
        "http://localhost:8080")

    humiditySensorOne = HumiditySensor(
        "humidity",
        IMPERIAL,
        "http://localhost:8080")

    print("Temperature in degrees {}: {}".format(temperatureSensorOne.getUnits(), temperatureSensorOne.getSensorValue()))

    print("Relative Humidity: ", humiditySensorOne.getSensorValue())
    print("Dew Point {}: {}".format(humiditySensorOne.getUnits(), humiditySensorOne.getDewPoint(temperatureSensorOne.getDegreesCelcius())))


def testSimulated():
    print("testing")
    temp = TemperatureSensor(sub_address="temperature")
    humid = HumiditySensor(sub_address="humidity")
    print(temp.getSensorValue())
    print(humid.getSensorValue())


if __name__ == "__main__":
    main()
    #testSimulated()
