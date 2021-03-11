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


    ### Config Structure ###

    # saveConfigData(sensor_type, name, category, address, port, sub_address, min_threshold, max_threshold, units, alerts)



    ##  Indoor Sensor Cluster   ##

    # SHT31
    data.saveConfigData("temperature", "Room Temperature", "Indoor Sensors", "10.0.1.60", 80, "temperature", -10, 50, "celsius", True)
    data.saveConfigData("humidity", "Room Humidity", "Indoor Sensors", "10.0.1.60", 80, "humidity", 30, 75, "percent", True)

    #DS18B20
    data.saveConfigData("temperature", "Inside Temperature 1", "Indoor Sensors", "10.0.1.60", 80, "sensor1", -10, 50, "celsius", True)
    data.saveConfigData("temperature", "Inside Temperature 2", "Indoor Sensors", "10.0.1.60", 80, "sensor2", -10, 50, "celsius", True)
    data.saveConfigData("temperature", "Inside Temperature 3", "Indoor Sensors", "10.0.1.60", 80, "sensor3", -10, 50, "celsius", True)
    data.saveConfigData("temperature", "Inside Temperature 4", "Indoor Sensors", "10.0.1.60", 80, "sensor4", -10, 50, "celsius", True)

    ##  Outdoor Sensor Cluster  ##

    # SHT31
    data.saveConfigData("temperature", "Back Porch Temperature", "Outdoor Sensors", "10.0.1.64", 80, "temperatureSHT", -10, 50, "celsius", True)
    data.saveConfigData("humidity", "Back Porch Humidity", "Outdoor Sensors", "10.0.1.64", 80, "humiditySHT", 30, 90, "percent", True)

    # DS18B20
    data.saveConfigData("temperature", "Outside Temperature 1", "Outdoor Sensors", "10.0.1.64", 80, "sensor1", -10, 50, "celsius", True)
    data.saveConfigData("temperature", "Outside Temperature 2", "Outdoor Sensors", "10.0.1.64", 80, "sensor2", -10, 50, "celsius", True)
    data.saveConfigData("temperature", "Outside Temperature 3", "Outdoor Sensors", "10.0.1.64", 80, "sensor3", -10, 50, "celsius", True)
    data.saveConfigData("temperature", "Outside Temperature 4", "Outdoor Sensors", "10.0.1.64", 80, "sensor4", -10, 50, "celsius", True)
    data.saveConfigData("temperature", "Kegerator Temperature", "Outdoor Sensors", "10.0.1.64", 80, "probe", -5, 40, "celsius", True)

    # DHT 22
    data.saveConfigData("temperature", "DHT One Temperature", "Outdoor Sensors", "10.0.1.64", 80, "dht1temperature", -10, 50, "celsius", True)
    data.saveConfigData("humidity", "DHT One Humidity", "Outdoor Sensors", "10.0.1.64", 80, "dht1humidity", 30, 90, "percent", True)
    data.saveConfigData("temperature", "DHT Two Temperature", "Outdoor Sensors", "10.0.1.64", 80, "dht2temperature", -10, 50, "celsius", True)
    data.saveConfigData("humidity", "DHT Two Humidity", "Outdoor Sensors", "10.0.1.64", 80, "dht2humidity", 30, 90, "percent", True)


if __name__ == "__main__":
    main()
