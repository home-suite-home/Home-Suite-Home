from configparser import ConfigParser
import json
import Sensors


we need to:
    - get the current sensors configuration
    - access a particular sensors
    - update a specific sensor data
    - remove a sensor
    - create a new sensor


parser = ConfigParser()
parser.read("sensors.config")

if parser.has_option("sensor_types", "types"):
    types = parser.get("sensor_types", "types")
    typesArray = json.loads(types)
    print("Types: ", typesArray)
else:
    print("types does not exist")

if parser.has_option("global", "units")
    units = parser.get("global", "units")
else
    units = "imperial"

if parser.has_option("sensor_types", "type_configs"):
    typesConfig = parser.get("sensor_types", "type_configs")
    typesConfigArray = json.loads(typesConfig)
    print("Types: ", typesConfigArray)
else:
    print("types does not exist")

for sensorConfigs in typesConfigArray:
    try:
        parser = ConfigParser()
        parser.read(sensorConfigs)
        print("new config file name: ", sensorConfigs)
    except:
        print("failed to open: ", sensorConfigs)

    # for sectionName in parser.sections():
    #     print("Section: ", sectionName)
    #     print("Options: ", parser.options(sectionName))
    #     for key, value in parser.items(sectionName):
    #         print('    {} = {}'.format(key, value))
    #     print()

    for sensorName in parser.sections():
        name = sensorName
        address = parser.get(sensorName, "address")
        plug = parser.get(sensorName, "sub_address")
        minThreshold = parser.get(sensorName, "minimum")
        maxThreshold = parser.get(sensorName, "maximum")
        alerts = parser.get(sensorName, "alerts")
        if "temperature" in sensorName.lower():
            temperatureSensor = TemperatureSensor(plug, units, address)
            print("temperature of ", sensorName, ": ", temperatureSensor.getSensorValue())
        elif "humidity" in sensorName.lower():
            humiditySensorOne = HumiditySensor(plug, units, address)
            print("humidity at ", sensorName, ": ", )




# for sectionName in parser.sections():
#     print("Section: ", sectionName)
#     print("Options: ", parser.options(sectionName))
#     for key, value in parser.items(sectionName):
#         print('    {} = {}'.format(key, value))
#     print()
