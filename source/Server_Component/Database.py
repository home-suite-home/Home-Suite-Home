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
			collection.insert_one(dataobj) # DIct is fine.
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()

	# Maybe per sensor querying

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

	
	def GetAvgVal(name)
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']
			records = collection.find({'name' : name}, {'_id' : 0 , 'name' : 0, 'type' : 0, 'value' : 1})
			
			value_list = []
			total = 0
			for record in records:
				#report = json.load(record)
				total += (float)record[value]
				print(record[value])
				
			sensor_avg = total / len(records)
				
			return sensor_avg
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return 0
	
	##
	def Clear():
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']
			
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()




def main():
	print('Testing...')
	dbase = Database(URL, POST)
	dbase.connect()		

if __name__ == "__main__":
	main()
