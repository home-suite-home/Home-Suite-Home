# Nathan Moulton
# Database.py

import pymongo as mongo
import json
import time


URL = 'localhost'
PORT = 27017

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
	def __init__(self, url, port):
		self.url = url
		self.port = port
		self.connect_status = False
		self.client = mongo.MongoClient()

	def connect(self):
		if self.connect_status == False:
			try:
				self.client = mongo.MongoClient(self.url, self.port)
				self.connect_status = True
			except ConnectionFailure:
				print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
				self.connect_status = False
		else:
			print("connection already established")
	
	# Populates the databas with a single recod given its name, sensor type, and raw value. 
	def SendSensorData(self, data, name, sensor_type):
		if self.connect_status == True:

			db = self.client['sensorsdb']
			collection = db['sensors']
			t = time.time()

			dataobj = {
                            "type": sensor_type,
                            "name": name,
                            "value": data,
                            "time": t
			}

			#payload = json.dumps(dataobj)
			collection.insert_one(dataobj) # Dict is fine for parsing. No JSON needed
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()

	# Retrieves all values currently in the database
	def GetData(self):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']
			records = collection.find({}, {'_id' : 0})
			report_list = []

			for record in records:
				#report = json.load(record)
				report_list.append(record)
				print(record)
				
			return report_list
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return []

	# Produces the average value of a sensor in the database
	def GetAvgVal(self, name):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']
			records = collection.find({'name' : name}, {'_id' : 0, 'time' : 0, 'type' : 0, 'name' : 0})
			total = 0
			num = collection.count_documents({'name' : name})
			value_list = []
			
			for record in records:
				print(record)
				total += float(record['value'])
				#report = json.load(record)
				
			sensor_avg = total / num
				
			return sensor_avg
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return 0
	
	# Deletes all records in the database
	def Clear(self):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']
			
			collection.delete_many({})
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
