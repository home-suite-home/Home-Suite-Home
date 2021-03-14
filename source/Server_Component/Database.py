# Nathan Moulton
# Database.py
import sys
sys.path.append("..")


import pymongo as mongo
from timeKeeper import TimeStamps


URL = 'localhost'
PORT = 27017


# This class will be comprised of methods that will
# interface with a MongoDB database. These methods should
# expect values from the methods in Sensors.py, and
# send them to the database as JSON payloads.

# Environmental Sensors

# Something Something sensors

# Industrial sensors

# RECENT UPDATES
#
# Get avg has time parameter
#
#
#

class Database:
	def __init__(self, url = URL, port = PORT):
		self.url = url
		self.port = port
		self.connect_status = False
		try:
			self.client = mongo.MongoClient(self.url, self.port)
			self.connect_status = True
		except Exception as e:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
		else:
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

	# Populates the database with a single recod given its name, sensor type, and raw value.
	def sendSensorData(self, data, name, sensor_type):
		if self.connect_status == True:

			db = self.client['sensorsdb']
			collection = db['sensors']
			ts = TimeStamps().getTimestamp()

			dataobj = {
                        	"type": sensor_type,
                        	"name": name,
                        	"value": data,
                        	"time": ts
			}

			collection.insert_one(dataobj)
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()

	# Retrieves all values currently in the database
	def getData(self):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']
			records = collection.find({}, {'_id' : 0})
			report_list = []

			for record in records:
				report_list.append(record)

			return report_list
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return []

	# Produces the average value of a sensor in a time period
	def getAvgVal(self, name, sensor_type):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']
			records = collection.find({'name' : name, 'type' : sensor_type}, {'_id' : 0, 'time' : 0, 'type' : 0, 'name' : 0})
			total = 0
			num = 0

			for record in records:
				total += record['value']
				num += 1

			try:
				sensor_avg = total / num
			except Exception as e:
				sensor_avg = 0

			return sensor_avg
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return 0


	# Saves/ Updates sensor config data
	def saveConfigData(self, sensor_type, name, category, address, port, sub_address, min_threshold, max_threshold, units, alerts):
		if self.connect_status == True:

			db = self.client['sensorsdb']
			collection = db['config']

			dataobj = {
                            "type": sensor_type,
                            "name": name,
							"category": category,
                            "address": address,
							"port": port,
                            "sub_address": sub_address,
                            "min_threshold" : min_threshold,
                            "max_threshold" : max_threshold,
							"units" : units,
                            "alerts": alerts
			}

			# First, check if there's a record for this sensor...
			if collection.count_documents({'name' : name, 'type' : sensor_type}) >= 1:
				# ... and update if there's an existing record
				collection.replace_one({'name' : name, 'type' : sensor_type}, dataobj)
			else:
				# Otherwise, insert the record
				collection.insert_one(dataobj)
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()


	# retrieves a sensor's data in the database within a range of hours
	def getRecentSensorData(self, name, sensor_type, hours):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']

			# All records will have a ts value greater than this
			time_bound = (TimeStamps().getTimestamp()) - (3600 * hours)
			records = collection.find({'name' : name, 'type' : sensor_type, 'time': {'$gte': time_bound}}, {'_id' : 0}).sort("time", -1)
			report_list = []

			for record in records:
				report_list.append(record)

			return report_list
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return []

	# Returns the most recent value for a given sensor
	def getMostRecentSensorData(self, name, sensor_type):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']
			record = collection.find_one({'name': name, 'type' : sensor_type }, sort = [('time', -1)])

			if record is None:
				return 0

			return record['value']
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return 0

	# Returns minimum value of a sensor in a certain time frame
	def getRecentMax(self, name, sensor_type, hours):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']

			# All records will have a ts value greater than this
			time_bound = (TimeStamps().getTimestamp()) - (3600 * hours)
			record = collection.find_one({'name': name, 'type' : sensor_type, 'time' : { '$gte' : time_bound }}, sort = [('value', -1)])

			if record is None:
				return 0

			return record['value']
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return 0

	# Returns minimum value of a sensor in a certain time frame
	def getRecentMin(self, name, sensor_type, hours):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']

			# All records will have a ts value greater than this
			time_bound = (TimeStamps().getTimestamp()) - (3600 * hours)
			record = collection.find_one({'name': name, 'type' : sensor_type,'time' : { '$gte' : time_bound }}, sort = [('value', 1)])

			if record is None:
				return 0

			return record['value']
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return 0

	# retrieves all config data
	def getConfigData(self):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['config']
			records = collection.find({}, {'_id' : 0})
			report_list = []

			for record in records:
				report_list.append(record)

			return report_list
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return []

	# returns an array of field tyes
	def getFields(self, field):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['config']
			records = collection.find({}, {'_id' : 0}).distinct(field)
			report_list = []

			for record in records:
				report_list.append(record)

			return report_list
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
			return []


	# removes a named sensor's config file
	def deleteConfigData(self, name, sensor_type):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['config']

			collection.delete_one({"name" : name, "type" : sensor_type})
			print("deleting " + name + " : " + sensor_type + " ...")
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()

	# Deletes all config data
	def clearConfigData(self):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['config']

			collection.delete_many({})
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()


	# Deletes all records in the database
	def clear(self):
		if self.connect_status == True:
			db = self.client['sensorsdb']
			collection = db['sensors']

			collection.delete_many({})
		else:
			print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
			self.connect()
