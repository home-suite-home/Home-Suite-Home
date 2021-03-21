# Engineer: Andres Graterol
import pytest
import mongomock
from alerts import Alert
from Database import *
from timeKeeper import * 

def test_subject(mongodb):
    assert 'config' in mongodb.list_collection_names()
    configuration = mongodb.config.find_one({'name':'temp_3'})
    alert = Alert(configuration, 62.5)
    subject_string = "Out of Tolerance Alert: temp_3 Value: 62.5"
    assert (alert._Alert__generate_subject() == subject_string)
    
def test_text_body(mongodb):
    assert 'config' in mongodb.list_collection_names()
    configuration = mongodb.config.find_one({'name':'temp_1'})
    ts = TimeStamps()
    alert = Alert(configuration, 50.3)
    body = "\nSensor Value Out of Tolerance\n\n"
    body += ts.getTimestampString()
    func_body = alert._Alert__generate_text_body()
    body += "\n\nName: "
    body += "temp_1"
    body += "\nType: "
    body += "temperature"
    body += "\nCategory: "
    body += "inside"
    body += "\n\nCurrent Value: "
    body += "122.54"
    body += "\nMax Threshold: "
    body += "60"
    body += "\nMin Threshold: "
    body += "10"
    body += "\n\nSensor Settings:"
    body += "\nIP Address: "
    body += "http: // localhost"
    body += "\nPort: "
    body += "8080"
    body += "\nSub Address: /"
    body += "temperature"
    body += "\nUnits: "
    body += "fahrenheit"
    body += "\nAlerts: "
    body += "True"
    body += "\n\n"
    print(func_body)
    print(body)
    assert (func_body == body)
