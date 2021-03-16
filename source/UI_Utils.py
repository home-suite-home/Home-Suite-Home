from HTTP_Component.Sensors import Sensor
import math

def isValidSensor(sensor_type, url_plug, ip_address, sensor_name, port='8080'):
    if(sensor_type == None):
        return False


    if(port == ''):
        port = '8080'

    print("{}:{}/{}".format(ip_address, port, url_plug))
    mySensor = Sensor(url_plug, domain=ip_address, port=port).getSensorValue()

    try:
        if(type(mySensor) == float and not math.isnan(mySensor)):
            return True
        else:
            return False
    except:
        return False
