#
#   Filename: timeKeeper.py
#   Date: 03/03/2021
#
#   Engineer: Wyatt Vining
#   Contact: wyatt.vining@knights.ucf.edu
#
#   Description: utility for getting and parsing time and date stamps
#

import time
import datetime

class TimeStamps:
    # returns an int - ready for storing in the database
    def getTimestamp(self):
        return int(time.time())

    # converts an int from a database into a time-date data object - ready to be parsed
    def stringToTimestamp(self, tstamp):
        timeString = str(datetime.datetime.fromtimestamp(tstamp))
        return datetime.datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S')

    # demonstrates use of timestamp data
    # expects a timedate data object - output of stringToTimestamp()
    def printTimestamp(self, timestamp):
        year = timestamp.strftime("%Y")
        print("year:", year)

        month = timestamp.strftime("%m")
        print("month:", month)

        day = timestamp.strftime("%d")
        print("day:", day)

        time = timestamp.strftime("%H:%M:%S")
        print("time:", time)

        date_time = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        print("date and time:",date_time)


def main():

    ts = TimeStamps()
    date_time_string = ts.getTimestamp() # a.k.a get the timestamp from the databse
    date_time_obj = ts.stringToTimestamp(date_time_string) # create a datetime data object from the timestamp string
    #print(date_time_string)
    ts.printTimestamp(date_time_obj) # parse and print the timedate data object

if __name__ == "__main__":
    main()
