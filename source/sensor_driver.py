import sys
from time import sleep
import timeKeeper
from HTTP_Component.Sensors import Sensor
from Server_Component.Database import Database
from EmailComponent.EmailController import EmailController
from settings import Settings
from alerts import Alert


POLL_RATE_DEFAULT = 60

def main():
    db = Database()
    config = Settings()

    poll_rate = config.get_int_setting("sensors", "poll_rate")
    silence_alerts = config.get_bool_setting("alerts", "rate_limit")

    if poll_rate <= 0:
        poll_rate = POLL_RATE_DEFAULT

    while True:
        sensorConfigs = db.getConfigData()
        
        for record in sensorConfigs:

            sensorValue = Sensor(url_plug = record["sub_address"], domain = record["address"]).getSensorValue()
            print(record["name"], ": ", sensorValue)

            if record["alerts"] is True and silence_alerts is False:
                if sensorValue == "NaN":
                    Alert(record, sensorValue).handleAlert()
                    print("Error recieving sensor data")
                elif sensorValue > record["max_threshold"] or sensorValue < record["min_threshold"]:
                    Alert(record, sensorValue).handleAlert()
                    print("Sensor value out of tollerance")

            db.sendSensorData(sensorValue, record["name"], record["type"])

        sleep(poll_rate)

if __name__ == "__main__":
    main()
