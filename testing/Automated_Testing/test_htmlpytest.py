'''
  Date: 02/19/2021
  FileName: test_htmlpytest.py
  
  Engineer: Andres Graterol
  Contact: graterol.andres0@knights.ucf.edu
  Description: 
    Provides automated unit tests for 
    the following functions in Sensors.py:
        TemperatureSensor.getSensorValue()
        HumiditySensor.getSensorValue()
        getDegreesCelsius()
        calculateDewPoint()
'''

# Automated Testing for Sensors.py
import pytest
from Sensors import *

def test_getDegreesCelsius():
    Temp = TemperatureSensor(url_plug="temperature")
    degrees = Temp.getDegreesCelcius()
    assert isinstance(degrees, float)

def test_calculateDewPoint():
    Humid = HumiditySensor(url_plug="humidity")
    assert Humid.calculateDewPoint(50.00, 25.00) == 13.85 
