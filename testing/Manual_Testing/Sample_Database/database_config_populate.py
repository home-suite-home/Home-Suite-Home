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


import Database
import Sensors

def main():

    data = Database.Database()

    # use data.clear() to remove all sensor data
    # data.Clear()

    # use data.ClearConfigData() to remove all config data
    # data.ClearConfigData()

    # SaveConfigData(categeory, type, name, address, port_number, sub_address, units, min_threshold, max_threshold, alerts)

    ##  Indoor Sensor Cluster   ##

    # SHT31
    data.SaveConfigData("temperature", "Room Temperature", "http://10.0.1.60", "temperature", -10, 50, True)
    data.SaveConfigData("humidity", "Room Humidity", "http://10.0.1.60", "humidity", 30, 75, True)

    #DS18B20
    data.SaveConfigData("temperature", "Inside Temperature 1", "http://10.0.1.60", "sensor1", -10, 50, True)
    data.SaveConfigData("temperature", "Inside Temperature 2", "http://10.0.1.60", "sensor2", -10, 50, True)
    data.SaveConfigData("temperature", "Inside Temperature 3", "http://10.0.1.60", "sensor3", -10, 50, True)
    data.SaveConfigData("temperature", "Inside Temperature 4", "http://10.0.1.60", "sensor4", -10, 50, True)

    ##  Outdoor Sensor Cluster  ##

    # SHT31
    data.SaveConfigData("temperature", "Back Porch Temperature", "http://10.0.1.64", "temperatureSHT", -10, 50, True)
    data.SaveConfigData("humidity", "Back Porch Humidity", "http://10.0.1.64", "humiditySHT", -10, 50, True)

    # DS18B20
    data.SaveConfigData("temperature", "Outside Temperature 1", "http://10.0.1.64", "sensor1", -10, 50, True)
    data.SaveConfigData("temperature", "Outside Temperature 2", "http://10.0.1.64", "sensor2", -10, 50, True)
    data.SaveConfigData("temperature", "Outside Temperature 3", "http://10.0.1.64", "sensor3", -10, 50, True)
    data.SaveConfigData("temperature", "Outside Temperature 4", "http://10.0.1.64", "sensor4", -10, 50, True)
    data.SaveConfigData("temperature", "Kegerator Temperature", "http://10.0.1.64", "probe", -5, 40, True)

    # DHT 22
    data.SaveConfigData("temperature", "DHT One Temperature", "http://10.0.1.64", "dht1temperature", -10, 50, True)
    data.SaveConfigData("humidity", "DHT One Humidity", "http://10.0.1.64", "dht1humidity", -10, 50, True)
    data.SaveConfigData("temperature", "DHT Two Temperature", "http://10.0.1.64", "dht2temperature", -10, 50, True)
    data.SaveConfigData("humidity", "DHT Two Humidity", "http://10.0.1.64", "dht2humidity", -10, 50, True)


if __name__ == "__main__":
    main()
