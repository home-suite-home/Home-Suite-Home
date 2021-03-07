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

    dbase.SaveConfigData("temperature", "temp_1",
                         "http: // localhost: 8080", "temperature", 10, 60, True)
    dbase.SaveConfigData("temperature", "temp_2",
                         "http: // localhost: 8080", "temperature", 10, 60, False)
    dbase.SaveConfigData("temperature", "temp_3",
                         "http: // localhost: 8080", "temperature", 10, 60, True)
    dbase.SaveConfigData("humidity", "humid_1",
                         "http: // localhost: 8080", "humidity", 30, 50, False)
    dbase.SaveConfigData("humidity", "humid_2",
                         "http: // localhost: 8080", "humidity", 30, 50, True)
    dbase.SaveConfigData("humidity", "humid_3",
                         "http: // localhost: 8080", "humidity", 30, 50, False)

    # Shows record of added config
    config_list = dbase.GetConfigData()

    # Deleting these sensor names
    print()
    dbase.DeleteConfigData("temp_3", "temperature")
    dbase.DeleteConfigData("humid_3", "humidity")

    # Ensuring that new records show removal
    config_list = dbase.GetConfigData()

    # uncomment this whenever you wish to clear the config database:
    #dbase.ClearConfigData()

    # Now testing sending configured sensor data
    print()
    print('Testing Sensors Collection...')

    # Populating the database with sensor data
    dbase.SendSensorData(10.0, "temp_1", "Temp")
    dbase.SendSensorData(20.0, "temp_2", "Temp")
    dbase.SendSensorData(30.0, "temp_3", "Temp")
    dbase.SendSensorData(10.0, "humid_1", "Humid")
    dbase.SendSensorData(20.0, "humid_2", "Humid")
    dbase.SendSensorData(30.0, "humid_3", "Humid")
    dbase.SendSensorData(10.0, "temp_1", "Temp")
    dbase.SendSensorData(20.0, "temp_2", "Temp")
    dbase.SendSensorData(30.0, "temp_3", "Temp")
    dbase.SendSensorData(10.0, "humid_1", "Humid")
    dbase.SendSensorData(20.0, "humid_2", "Humid")
    dbase.SendSensorData(30.0, "humid_3", "Humid")

    # Prints all the records of the database
    test_list = dbase.GetData()

    # Checking temperature sensor data
    tempTest_value1 = dbase.GetAvgVal("temp_1", "temperature")
    tempTest_value2 = dbase.GetAvgVal("temp_2", "temperature")
    tempTest_value3 = dbase.GetAvgVal("temp_3", "temperature")
    print("Average for temp_1: " + str(tempTest_value1))
    print("Average for temp_2: " + str(tempTest_value2))
    print("Average for temp_3: " + str(tempTest_value3))

    # Checking humidity sensor data
    humidTest_value1 = dbase.GetAvgVal("humid_1", "humidity")
    humidTest_value2 = dbase.GetAvgVal("humid_2", "humidity")
    humidTest_value3 = dbase.GetAvgVal("humid_3", "humidity")
    print("Average for humid_1: " + str(humidTest_value1))
    print("Average for humid_2: " + str(humidTest_value2))
    print("Average for humid_3: " + str(humidTest_value3))
    print()

    # Print timestamp for every second (20)
    for i in range(20):
        ts = TimeStamps.getTimestamp(TimeStamps)
        n = 50 + (i % 5)
        dbase.SendSensorData(n, "outside_1", "temperature")
        print(ts)
        time.sleep(1)

    sensors = dbase.GetRecentSensorData(
        'outside_1', 'temperature', (5 * 0.00028))
    print()

    # Show that the last 5 timestamps are obtained using the
    # GetRecentSensorData function
    for sensor in sensors:
        print(sensor)

    # uncomment this whenever you wish to clear the sensors database:
    #dbase.Clear()


test_db()
