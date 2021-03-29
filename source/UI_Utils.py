from HTTP_Component.Sensors import Sensor
from Server_Component.Database import Database
import math

db = Database()

def isValidSensor(sensor_type, url_plug, ip_address, sensor_name, port='80'):
    #print("{}:{}/{}".format(ip_address, port, url_plug))

    if(sensor_type == None):
        return False

    if(db.getSensorConfig(sensor_name, sensor_type)):
        return False

    if(port == ''):
        port = '80'

    mySensor = Sensor(url_plug, domain=ip_address, port=port).getSensorValue()
    #print("mySensor: {}, type: {}".format(mySensor, type(mySensor)))

    if(math.isnan(mySensor)):
        return False

    return True
