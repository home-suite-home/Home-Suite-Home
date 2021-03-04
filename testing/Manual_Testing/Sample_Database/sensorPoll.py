import Database
import Sensors
from time import sleep

data = Database.Database()

def main():
    configs = data.GetConfigData()
    loopCounter = 1;

    while True:
        print()
        print()
        print("=============================")
        print("LOOP: ", loopCounter)
        print("=============================")
        print()
        for record in configs:
            print("------------------------------")
            print()
            type = record["type"]
            name = record["name"]
            print(name)
            address = record["address"]
            sub_address = record["sub_address"]
            min_threshold = record["min_threshold"]
            max_threshold = record["max_threshold"]
            sensorValue = Sensors.Sensor(sub_address, "metric", address).getSensorValue()
            print(sensorValue)
            data.SendSensorData(sensorValue, name, type)
            print()
        loopCounter += 1
        sleep(60)

if __name__ == "__main__":
    main()
