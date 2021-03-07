import sys
from time import sleep
import timeKeeper
from HTTP_Component.Sensors import Sensor
from Server_Component.Database import Database
from EmailComponent.EmailController import EmailController


POLL_RATE = 60

def main():
    db = Database()
    sensorConfigs = db.GetConfigData()

    while True:
        for record in sensorConfigs:

            sensorValue = Sensor(url_plug = record["sub_address"], domain = record["address"]).getSensorValue()
            print(record["name"], ": ", sensorValue)

            if sensorValue == "NaN":
                # TODO: send email alert
                print("Error recieving sensor data")
            elif sensorValue > record["max_threshold"] or sensorValue < record["min_threshold"]:
                # TODO: send email alert
                print("Sensor value out of tollerance")

            db.SendSensorData(sensorValue, record["name"], record["type"])

        sleep(POLL_RATE)

if __name__ == "__main__":
    main()
