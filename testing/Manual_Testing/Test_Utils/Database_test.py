# Manual test for Database.py
import pytest
from Database import *
import time

def test_db():
    print('Testing...')
    URL = 'localhost' 
    PORT = 27017
    dbase = Database(URL, PORT)
    dbase.connect()
	
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
    tempTest_value1 = dbase.GetAvgVal("temp_1")
    tempTest_value2 = dbase.GetAvgVal("temp_2")
    tempTest_value3 = dbase.GetAvgVal("temp_3")
    print("Average for temp_1: " + str(tempTest_value1))
    print("Average for temp_2: " + str(tempTest_value2))
    print("Average for temp_3: " + str(tempTest_value3))

    # Checking humidity sensor data 
    humidTest_value1 = dbase.GetAvgVal("humid_1")
    humidTest_value2 = dbase.GetAvgVal("humid_2")
    humidTest_value3 = dbase.GetAvgVal("humid_3")
    print("Average for humid_1: " + str(humidTest_value1))
    print("Average for humid_2: " + str(humidTest_value2))
    print("Average for humid_3: " + str(humidTest_value3))

    # uncomment this whenever you wish to clear the database:
    #dbase.Clear()

test_db()

