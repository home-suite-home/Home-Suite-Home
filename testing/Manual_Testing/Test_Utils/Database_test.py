# Manual test for Database.py
import pytest
from Database import *
import time


def test_db():
    URL = 'localhost'
    PORT = 27017
    dbase = Database(URL, PORT)
    dbase.connect()

    # Testing the configuration functions
    print("Testing Config Collection...")

    dbase.saveConfigData("temperature", "temp_1", "inside", 
                         "http: // localhost", "8080", "temperature", 10, 60, "fahrenheit", True)
    dbase.saveConfigData("temperature", "temp_2", "outside",
                         "http: // localhost", "8080", "temperature", 10, 60, "fahrenheit", False)
    dbase.saveConfigData("temperature", "temp_3", "inside",
                         "http: // localhost", "8080", "temperature", 10, 60, "celsius", True)
    dbase.saveConfigData("humidity", "humid_1", "outside"
                         "http: // localhost", "8080", "humidity", 30, 50, "percent", False)
    dbase.saveConfigData("humidity", "humid_2", "inside"
                         "http: // localhost", "8080", "humidity", 30, 50, "percent", True)
    dbase.saveConfigData("humidity", "humid_3", "outside"
                         "http: // localhost", "8080", "humidity", 30, 50, "percent", False)

    # Shows record of added config
    config_list = dbase.getConfigData()
    print(config_list)

    # Deleting these sensor names
    print()
    dbase.deleteConfigData("temp_3", "temperature")
    dbase.deleteConfigData("humid_3", "humidity")

    # Ensuring that new records show removal
    config_list = dbase.getConfigData()
    print(config_list)

    # uncomment this whenever you wish to clear the config database:
    #dbase.clearConfigData()

    # Now testing sending configured sensor data
    print()
    print('Testing Sensors Collection...')

    # Populating the database with sensor data
    dbase.sendSensorData(10.0, "temp_1", "Temp")
    dbase.sendSensorData(20.0, "temp_2", "Temp")
    dbase.sendSensorData(30.0, "temp_3", "Temp")
    dbase.sendSensorData(10.0, "humid_1", "Humid")
    dbase.sendSensorData(20.0, "humid_2", "Humid")
    dbase.sendSensorData(30.0, "humid_3", "Humid")
    dbase.sendSensorData(10.0, "temp_1", "Temp")
    dbase.sendSensorData(20.0, "temp_2", "Temp")
    dbase.sendSensorData(30.0, "temp_3", "Temp")
    dbase.sendSensorData(10.0, "humid_1", "Humid")
    dbase.sendSensorData(20.0, "humid_2", "Humid")
    dbase.sendSensorData(30.0, "humid_3", "Humid")

    # Prints all the records of the database
    test_list = dbase.getData()
    print(test_list)
    print()

    # Checking temperature sensor data
    tempTest_value1 = dbase.getAvgVal("temp_1", "Temp")
    tempTest_value2 = dbase.getAvgVal("temp_2", "Temp")
    tempTest_value3 = dbase.getAvgVal("temp_3", "Temp")
    print("Average for temp_1: " + str(tempTest_value1))
    print("Average for temp_2: " + str(tempTest_value2))
    print("Average for temp_3: " + str(tempTest_value3))

    # Checking humidity sensor data
    humidTest_value1 = dbase.getAvgVal("humid_1", "Humid")
    humidTest_value2 = dbase.getAvgVal("humid_2", "Humid")
    humidTest_value3 = dbase.getAvgVal("humid_3", "Humid")
    print("Average for humid_1: " + str(humidTest_value1))
    print("Average for humid_2: " + str(humidTest_value2))
    print("Average for humid_3: " + str(humidTest_value3))
    print()

    # Print timestamp for every second (20)
    for i in range(20):
        ts = TimeStamps.getTimestamp(TimeStamps)
        n = 50 + (i % 5)
        dbase.sendSensorData(n, "outside_1", "temperature")
        print(ts)
        time.sleep(1)

    sensors = dbase.getRecentSensorData(
        'outside_1', 'temperature', (5 * 0.00028))
    print()

    # Show that the last 5 timestamps are obtained using the
    # getRecentSensorData function
    for sensor in sensors:
        print(sensor)

    # uncomment this whenever you wish to clear the sensors database:
    #dbase.clear()


test_db()
