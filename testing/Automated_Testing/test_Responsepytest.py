#
# Date: 03/09/2021
# Filename: test_Responsepytest.py
#
# Engineer: Andres Graterol
# Contact: graterol.andres0@knights.ucf.edu
#
# Description: 
#
#
#
#

# Automated testing for CommandResponse.py
import pytest
from CommandResponse import *
from Database import *

def test_helpResponse():
    help_rqst = "help"
    help_response = CommandResponse(help_rqst)
    response_list = help_response.get_response()
    assert(response_list[0] == "dummy help message")

def test_sensorResponse():
    snsr_rqst = "get sensor data: Temp, temp_1, 20"
    snsr_response = CommandResponse(snsr_rqst)
    snsrResponse_list = snsr_response.get_response()
    assert(snsrResponse_list[2] != None)
