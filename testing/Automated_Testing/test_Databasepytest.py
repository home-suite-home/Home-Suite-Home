# Andres Graterol
# graterol.andres0@knights.ucf.edu
# This is a remake of the manual Database_test.py file 
# Automated testing for Database.py
from time import sleep
import pytest
import mongomock
from Database import *
from timeKeeper import *
 

# Test of the existing config collection
def test_ConfigData(mongodb):
    assert 'config' in mongodb.list_collection_names()
    configuration = mongodb.config.find_one({'name':'temp_1'})
    assert configuration['type'] == 'temperature'

# Test of the existing sensors collection
def test_SensorData(mongodb):
    assert 'sensors' in mongodb.list_collection_names()
    sensor = mongodb.sensors.find_one({'name':'temp_1'})
    assert sensor['type'] == 'Temp'

def test_insertData(mongodb):
    assert 'sensors' in mongodb.list_collection_names()
    ts = TimeStamps()
    dataobj = {
                    "type": "Temp",
                    "name": "temp_4",
                    "value": 30,
                    "time": ts.getTimestamp()
    }

    mongodb.sensors.insert_one(dataobj)
    sensor = mongodb.sensors.find_one({'name':'temp_4'})
    assert sensor['type'] == 'Temp'

def test_removeData(mongodb):
    assert 'sensors' in mongodb.list_collection_names()
    mongodb.sensors.delete_one({'name':'temp_4'})
    sensor = mongodb.sensors.find_one({'name':'temp_4'})
    assert sensor == None

def test_uniqueFields(mongodb):
    assert 'config' in mongodb.list_collection_names()
    records = mongodb.config.find({}).distinct("type")
    assert len(records) == 2

def test_recentData(mongodb):
    assert 'sensors' in mongodb.list_collection_names()
    ts = TimeStamps()
    dataobj = {
                    "type": "Humid",
                    "name": "humid_4",
                    "value": 12,
                    "time": ts.getTimestamp()
    }
    sleep(1)
    dataobj_2 = {
                    "type": "Humid",
                    "name": "humid_4",
                    "value": 10,
                    "time": ts.getTimestamp()
    }
    mongodb.sensors.insert_one(dataobj)
    mongodb.sensors.insert_one(dataobj_2)
    record = mongodb.sensors.find_one({"name":"humid_4", "type":"Humid"}, sort = [("time", -1)])
    assert record["value"] == 10

def test_alertSent(mongodb):
    assert 'logs' in mongodb.list_collection_names()
    ts = TimeStamps()
    timer = ts.getTimestamp()
    dataobj = {
                    "name": "Humid_5", 
                    "type": "Humid",
                    "time": timer
    }
    mongodb.logs.insert_one(dataobj)
    sleep(2)
    filter = {
                    "name": "Humid_5",
                    "type": "Humid",
                    "time" : {"$gte" : timer-2}
    }
    assert(mongodb.logs.count_documents(filter) >= 1)