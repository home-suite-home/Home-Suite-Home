import sys
sys.path.append('.')
sys.path.append('../Server_Component')
sys.path.append('../AnalyticsComponent')

from CommandResponse import CommandResponse
from Database import Database
from LineGraph import with_buttons
from LineGraph import data_over_time
import time

if len(sys.argv) < 2:
    print("No arguments entered")
    exit

elif sys.argv[1] == "--help":
    print("Starting help menu response testing:")
    resp = CommandResponse("help")
    print(resp.get_response())
    print("Help menu response testing complete")

elif sys.argv[1] == "--mostrecent":
    print("Starting most recent response testing:")
    # load the database
    db = Database()

    # call the command response
    resp = CommandResponse("get most recent sensor data")
    print(resp.get_response())

    print("most recent data response testing complete")

elif sys.argv[1] =="--getsensordata":
    print("Starting get sensor data response testing:")
    # load the database
    import time
    import random

    db = Database()
    db.saveConfigData("temperature", "temp_1", "", "", "", "",  0, 50, "", False)
    db.saveConfigData("temperature", "temp_2", "", "", "", "",  0, 50, "", False)

    for i in range(10):
        db.sendSensorData(random.randrange(6), "temp_1", "temperature")
        db.sendSensorData(random.randrange(70), "temp_2", "temperature")
        db.sendSensorData(random.randrange(10), "hum_1", "humidity")
        print(i)
        time.sleep(1)

    # call the command response
    #resp = CommandResponse("get sensor data: temperature, temp_2, 1")
    resp = with_buttons("temperature", "temp_2")
    #print(resp.get_response())
    resp.show()

    # reset databse
    #db.deleteConfigData("temp_1", "temperature")
    #db.deleteConfigData("temp_2", "temperature")
    print("get sensor data response testing complete")

elif sys.argv[1] =="--silencealerts":
    print("starting silence alerts test")
    resp = CommandResponse("silence alerts")
    print(resp.get_response())
    print("silence alerts testing complete")

elif sys.argv[1] =="--resumealerts":
    print("starting resume alerts test")
    resp = CommandResponse("resume alerts")
    print(resp.get_response())
    print("resume alerts testing complete")

else:
    print('Argument(s) passed: {}'.format(str(sys.argv)))
