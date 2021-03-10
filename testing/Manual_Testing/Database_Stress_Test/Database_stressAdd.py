import Database
import Sensors

def main():

    nameArray = "temp_0", "temp_1", "temp_2", "temp_3", "temp_4", "temp_5", "temp_6", "temp_7", "temp_8", "temp_9"

    data = Database.Database()

    temperatureSensorOne = Sensors.TemperatureSensor(
        "temperature",
        "imperial",
        "http://localhost:8080")
    for sensorName in nameArray:
        for i in range(100000):
            data.sendSensorData(temperatureSensorOne.getSensorValue(), sensorName, "temperature")

if __name__ == "__main__":
    main()
