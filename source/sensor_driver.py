import sys
from time import sleep
import timeKeeper
from HTTP_Component.Sensors import Sensor
from Server_Component.Database import Database
from EmailComponent.EmailController import EmailController
from settings import Settings
from alerts import Alert
from conversions import Units
from numbers import Number


POLL_RATE_DEFAULT = 60

def main():
    db = Database()
    config = Settings()

    poll_rate = config.get_int_setting("sensors", "poll_rate")
    silence_alerts = config.get_bool_setting("alerts", "silence_alerts")

    if poll_rate <= 0:
        poll_rate = POLL_RATE_DEFAULT

    while True:
        sensorConfigs = db.getConfigData()

        if sensorConfigs is []:
            continue
        
        for record in sensorConfigs:

            units = Units(record["type"], record["units"])

            sensorValue = Sensor(url_plug = record["sub_address"], domain = record["address"]).getSensorValue()
            print(record["name"], ": ", sensorValue)

            if record["alerts"] is True and silence_alerts is False:
                if isinstance(sensorValue, Number) is False:
                    Alert(record, sensorValue).handleAlert()
                    print("Error recieving sensor data")
                elif units.convert(sensorValue) > record["max_threshold"] or units.convert(sensorValue) < record["min_threshold"]:
                    Alert(record, sensorValue).handleAlert()
                    print("Sensor value out of tollerance")

            db.sendSensorData(sensorValue, record["name"], record["type"])

        sleep(poll_rate)

if __name__ == "__main__":
    main()
