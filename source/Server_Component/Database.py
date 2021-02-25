# Nathan Moulton
# Database.py

import pymongo as mongo
import json
import time


URL = 'localhost'
PORT = '27017'

#client = mongo.Mongoclient('localhost', 27017)
#db = client['sensorsdb']

# This class will be comprised of methods that will
# interface with a MongoDB database. These methods should
# expect values from the methods in Sensors.py, and 
# send them to the database as JSON payloads.

# Environmental Sensors

# Something Something sensors

# Industrial sensors


class Database:
	def _init_(self, url, port):
		self.url = url
		self.port = port
		self.connect_status = False
		self.client = mongo.MongoClient()
		
	def connect(void):
	# Add if statement based on status
		try:
			self.client = mongo.MongoClient(self.url, self.port)
			self.connect_status = True
		except ConnectionFailure
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
	
	# Maybe timestamp should be provided by sensor?		
	def SendSensorData(data):
		if (self.connect_status)
			
			db = self.client[sensorsdb]
			collection = db['temp']
			t = time.time()
			
			dataobj = {
			"name": "Temp_1"
			"temp": data
			"time": t 
			}
			
			payload = json.dumps(dataobj)
			collection.instert_one(payload)
		else
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")	
		
			
			
	def GetData():
		#TO BE ADDED
		
	def DeleteAll():
		
			
			
			
		
