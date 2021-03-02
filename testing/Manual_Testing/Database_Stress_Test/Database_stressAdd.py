import Database
import Sensors

def main():

    data = Database.Database()

    temperatureSensorOne = Sensors.TemperatureSensor(
        "temperature",
        "imperial",
        "http://localhost:8080")

    for i in range(45000):
        data.SendSensorData(temperatureSensorOne.getSensorValue(), "Outdoor Temperature", "temperature")

if __name__ == "__main__":
    main()
