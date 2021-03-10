#
#   Filename: databse_config_populate.py
#   Date: 3/5/21
#
#   Engineer: Wyatt Vining
#   Contact: wyatt.vining@knights.ucf.edu
#
#   Description:
#       Temporary method to create config files in the databse.
#       Will be replaced by user entry into the UI.
#


import sys
sys.path.insert(1, "../../../source")
import timeKeeper
sys.path.insert(1, "../../../source/HTTP_Component")
import Sensors
sys.path.insert(1, "../../../source/Server_Component")
import Database

def main():

    data = Database.Database()

    # use data.clear() to remove all sensor data
    # data.clear()

    # use data.clearConfigData() to remove all config data
    # data.clearConfigData()


    ### New Config Structure ###

    # saveConfigData(Categeory, type, name, IP_Address, port, url_plug sensor_units, min_threshold, max_threshold, alerts)
    # saveConfigData("Temperature", "temperature", "Outside Temperature", "10.0.1.60", 80, "sensor1", "Fahrenheit", min_threshold, max_threshold, alerts)



    ##  Indoor Sensor Cluster   ##

    # SHT31
    data.saveConfigData("temperature", "Room Temperature", "10.0.1.60", "temperature", -10, 50, True)
    data.saveConfigData("humidity", "Room Humidity", "10.0.1.60", "humidity", 30, 75, True)

    #DS18B20
    data.saveConfigData("temperature", "Inside Temperature 1", "10.0.1.60", "sensor1", -10, 50, True)
    data.saveConfigData("temperature", "Inside Temperature 2", "10.0.1.60", "sensor2", -10, 50, True)
    data.saveConfigData("temperature", "Inside Temperature 3", "10.0.1.60", "sensor3", -10, 50, True)
    data.saveConfigData("temperature", "Inside Temperature 4", "10.0.1.60", "sensor4", -10, 50, True)

    ##  Outdoor Sensor Cluster  ##

    # SHT31
    data.saveConfigData("temperature", "Back Porch Temperature", "10.0.1.64", "temperatureSHT", -10, 50, True)
    data.saveConfigData("humidity", "Back Porch Humidity", "10.0.1.64", "humiditySHT", 30, 90, True)

    # DS18B20
    data.saveConfigData("temperature", "Outside Temperature 1", "10.0.1.64", "sensor1", -10, 50, True)
    data.saveConfigData("temperature", "Outside Temperature 2", "10.0.1.64", "sensor2", -10, 50, True)
    data.saveConfigData("temperature", "Outside Temperature 3", "10.0.1.64", "sensor3", -10, 50, True)
    data.saveConfigData("temperature", "Outside Temperature 4", "10.0.1.64", "sensor4", -10, 50, True)
    data.saveConfigData("temperature", "Kegerator Temperature", "10.0.1.64", "probe", -5, 40, True)

    # DHT 22
    data.saveConfigData("temperature", "DHT One Temperature", "10.0.1.64", "dht1temperature", -10, 50, True)
    data.saveConfigData("humidity", "DHT One Humidity", "10.0.1.64", "dht1humidity", 30, 90, True)
    data.saveConfigData("temperature", "DHT Two Temperature", "10.0.1.64", "dht2temperature", -10, 50, True)
    data.saveConfigData("humidity", "DHT Two Humidity", "10.0.1.64", "dht2humidity", 30, 90, True)


if __name__ == "__main__":
    main()
