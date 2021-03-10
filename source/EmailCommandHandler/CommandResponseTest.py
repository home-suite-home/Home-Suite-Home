import sys
sys.path.append('.')
sys.path.append('../Server_Component')

from CommandResponse import CommandResponse
from Database import Database
import time

if sys.argv[1] == "--help":
    print("Starting help menu response testing:")
    resp = CommandResponse("help")
    print(resp.get_response())
    print("Help menu response testing complete")

elif sys.argv[1] == "--mostrecent":
    print("Starting most recent response testing:")
    # load the database
    db = Database()
    # storing config data for ONLY SENSORS 1 AND 2
    db.SaveConfigData("temperature", "temp_1", "local", "more_local", 0, 50, False)
    db.SaveConfigData("temperature", "temp_2", "local", "more_local", 0, 50, False)

    # storing sensor data
    db.SendSensorData(10.0, "temp_1", "temperature")
    db.SendSensorData(10.0, "temp_2", "temperature")
    db.SendSensorData(10.0, "temp_3", "temperature")
    time.sleep(2)
    db.SendSensorData(20.0, "temp_1", "temperature")
    db.SendSensorData(20.0, "temp_2", "temperature")
    db.SendSensorData(20.0, "temp_3", "temperature")

    # call the command response
    resp = CommandResponse("get most recent sensor data")
    print(resp.get_response())

    # reset databse
    db.Clear()
    db.DeleteConfigData("temp_1", "temperature")
    db.DeleteConfigData("temp_2", "temperature")
    print("most recent data response testing complete")

elif sys.argv[1] =="--getsensordata":
    print("Starting get sensor data response testing:")
    # load the database
    db = Database()
    # storing config data for ONLY SENSORS 1 AND 2
    db.SaveConfigData("temperature", "temp_1", "local", "more_local", 0, 50, False)
    db.SaveConfigData("temperature", "temp_2", "local", "more_local", 0, 50, False)

    # storing sensor data
    db.SendSensorData(10.0, "temp_1", "temperature")
    db.SendSensorData(10.0, "temp_2", "temperature")
    db.SendSensorData(10.0, "temp_3", "temperature")
    time.sleep(2)
    db.SendSensorData(20.0, "temp_1", "temperature")
    db.SendSensorData(20.0, "temp_2", "temperature")
    db.SendSensorData(20.0, "temp_3", "temperature")

    # call the command response
    resp = CommandResponse("get sensor data: temperature, temp_3, 1")
    print(resp.get_response())

    # reset databse
    db.Clear()
    db.DeleteConfigData("temp_1", "temperature")
    db.DeleteConfigData("temp_2", "temperature")
    print("get sensor data response testing complete")


else:
    print('Argument(s) passed: {}'.format(str(sys.argv)))
