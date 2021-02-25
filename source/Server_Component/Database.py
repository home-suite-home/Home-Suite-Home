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

	def connect(self):
		if not self.connect_status == True:
			try:
				self.client = mongo.MongoClient(self.url, self.port)
				self.connect_status = True
			except ConnectionFailure:
				print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
				self.connect_status = False
		else:
			print("connection already established")

	def SendSensorData(self, data, name, kind):
		if self.connect_status == True:

			db = self.client[sensorsdb]
			collection = db[sensors]
			t = time.time()

			dataobj = {
                            "kind": kind,
                            "name": name,
                            "value": data,
                            "time": t
			}

			payload = json.dumps(dataobj)
			collection.insert_one(payload)
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()

	# Maybe per sensor querying

	def GetData(self):
		if self.connect_status == True:
			db = self.client[sensorsdb]
			collection = db[sensors]
			records = collection.find({})

			for record in records:
				print(record)
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()

	##def DeleteAll():
		#TBD
