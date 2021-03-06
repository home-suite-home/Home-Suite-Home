# Nathan Moulton
# Database.py
import sys
sys.path.append("..")


import pymongo as mongo
from timeKeeper import TimeStamps
from Server_Component.Security import Security


URL = 'localhost'
PORT = 27017


# This class will be comprised of methods that will
# interface with a MongoDB database. These methods should
# expect values from the methods in Sensors.py, and
# send them to the database as JSON payloads.



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

        self.secure = Security(self.client)
        self.secure.setup()

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

            # ceate indexes to speed up common queries
            collection.create_index([("name", -1), ("type" , 1)])
            collection.create_index([("name", -1), ("type" , 1), ("time" , -1)])

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
                collection.update_one({'name' : name, 'type' : sensor_type}, {'$set' :dataobj})
            else:
                # Otherwise, insert the record
                collection.insert_one(dataobj)
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()

    # Recieves old document (given by getSensorConfig or a dict) as well as the fields of the updated records
    # And supplants them in the old record
    def editConfigData(self, doc, sensor_type, name, category, address, port, sub_address, min_threshold, max_threshold, units, alerts):
        if self.connect_status == True:

            db = self.client['sensorsdb']
            collection = db['config']
            sensor_collection = db['sensors']

            # Enforce unique name-type pairs
            collection.create_index([("name", -1), ("type" , 1)], unique = True)

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

            try:
                # LOL big fix for historical sensor data
                if doc["name"] != name:
                    collection.update_one(doc, {'$set' : dataobj})
                    sensor_collection.update_many({"name" : doc["name"]} , {'$set' : {'name' : name}})
                else:
                    collection.update_one(doc, {'$set' : dataobj})
            except Exception as e:
                print("Error in db: ", e)
                print("Entry already exists.")

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

            if record is None or str(record['value']) == 'nan':
                return 'NaN'


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

            if record is None or str(record['value']) == 'nan':
                return 'NaN'

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

            if record is None or str(record['value']) == 'nan':
                return 'NaN'

            return record['value']
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()
            return 0

    # Retrieves config doc for a sensor
    def getSensorConfig(self, name, sensor_type):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['config']
            record = collection.find_one({"name" : name, "type" : sensor_type})

            return record
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()
            return None

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

    # Add encryption: Saves pi credentials
    def saveCredentials(self, email, password):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['creds']

            crypt = self.client['encryption']['__homeSuiteKeyVault']
            crypt.drop()

            dataobj = {
                "email": email,
                "password" : self.secure.getEncryptedField(password, 1)
            }

            # First, check if there's a record for this sensor...
            if collection.count_documents({}) >= 1:
                # ... and update if there's an existing record
                collection.replace_one({}, dataobj)
            else:
                # Otherwise, insert the record
                collection.insert_one(dataobj)
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()


    def getCredentials(self):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['creds']
            record = collection.find_one({}, {'_id' : 0})
            if not record:
                return None
            password = record['password']
            record['password'] = self.secure.getDecryptedField(password)
            return record
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()
            return None

    # Saves user info to users collection.
    def saveUser(self, name, email):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['users']

            dataobj = {
                "name" : name,
                "email": email
            }

            # First, check if there's a record for this sensor...
            if collection.count_documents({'email' : email}) >= 1:
                # ... and update if there's an existing record
                collection.replace_one({'email' : email}, dataobj)
            else:
                # Otherwise, insert the record
                collection.insert_one(dataobj)
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()

    # returns dict of user doc comprised of name and email
    def getUser(self, email):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['users']
            record = collection.find_one({"email" : email})

            return record
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()
            return None

    def getAllUsers(self):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['users']
            records = collection.find({}, {'_id' : 0})

            report_list = []

            for record in records:
                report_list.append(record)

            return report_list
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()
            return []


    def deleteUser(self, email):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['users']

            collection.delete_one({ "email" : email})
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()

    def clearUsers(self):
        def deleteUser(self, email):
            if self.connect_status == True:
                db = self.client['sensorsdb']
                collection = db['users']

                collection.delete_many({})
            else:
                print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
                self.connect()

    # Saves an entry in alert logs
    def saveLog(self, name, sensor_type):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['logs']
            ts = TimeStamps().getTimestamp()

            dataobj = {
                            "type": sensor_type,
                            "name": name,
                            "time": ts
            }

            collection.insert_one(dataobj)
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()

    # returns True if an alert has already been sent in the user-defined
    # time frame, and False otherwise
    def alertSent(self, name, sensor_type, minutes):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['logs']
            time_bound = (TimeStamps().getTimestamp()) - (60 * minutes)

            filter = {
                        'name': name,
                        'type' : sensor_type,
                        'time' : {'$gte' : time_bound}
                        }

            if collection.count_documents(filter) >= 1:
                return True
            else:
                return False
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()
            return True

    # clears alert log
    def clearLog(self):
        if self.connect_status == True:
            db = self.client['sensorsdb']
            collection = db['logs']

            collection.delete_many({})
        else:
            print("Well that didn't work. Check the database address, and make sure the mongod process is running...")
            self.connect()

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
