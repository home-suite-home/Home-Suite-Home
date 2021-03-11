import sys
sys.path.insert(1, "../../../source")
import timeKeeper
sys.path.insert(1, "../../../source/HTTP_Component")
import Sensors
sys.path.insert(1, "../../../source/Server_Component")
import Database
from time import sleep

data = Database.Database()

def main():
    loopCounter = 1;

    while True:
        print()
        print()
        print("=============================")
        print("LOOP: ", loopCounter)
        print("=============================")
        print()
        configs = data.getConfigData()
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
            sensorValue = Sensors.Sensor(url_plug=sub_address, domain='localhost', port='8080').getSensorValue()
            print(sensorValue)
            data.sendSensorData(sensorValue, name, type)
            print()
        loopCounter += 1
        sleep(60)

if __name__ == "__main__":
    main()
