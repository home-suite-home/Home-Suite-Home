from HTTP_Component.Sensors import Sensor
from Server_Component.Database import Database
import math

db = Database()

def isValidSensor(sensor_type, url_plug, ip_address, newName, min_bound, max_bound, alert, 
        oldName='', port='80'):
    #print("{}:{}/{}".format(ip_address, port, url_plug))

    newNameExists = db.getSensorConfig(newName, sensor_type) != None

    if(newNameExists and oldName != newName):
        return False

    if(sensor_type == None):
        return False

    print(alert)
    if(alert):
        if(type(min_bound) == str or type(max_bound) == str):
            return False
        if(min_bound >= max_bound):
            return False


    if(port == ''):
        port = '80'

    mySensor = Sensor(url_plug, domain=ip_address, port=port).getSensorValue()
    #print("mySensor: {}, type: {}".format(mySensor, type(mySensor)))

    if(math.isnan(mySensor)):
        return False

    return True
