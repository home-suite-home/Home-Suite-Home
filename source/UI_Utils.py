from HTTP_Component.Sensors import Sensor
import math

def isValidSensor(url_plug, ip_address, port='8080'):
    if(port == ''):
        port = 8080
    mySensor = Sensor(url_plug, domain=ip_address, port=port).getSensorValue()

    try:
        if(type(mySensor) == float and not math.isnan(mySensor)):
            return True
        else:
            return False
    except:
        return False
