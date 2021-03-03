#
#   Filename: timeKeeper.py
#   Date: 03/03/2021
#
#   Engineer: Wyatt Vining
#   Contact: wyatt.vining@knights.ucf.edu
#
#   Description: utility for getting and parsing time and date stamps
#

import datetime

class TimeStamps:
    # returns a string - ready for storing in the database
    def getTimestampString(self):
        return str(datetime.datetime.now())

    # converts a string from a database into a time-date data object - ready to be parsed
    def stringToTimestamp(self, timeString):
        return datetime.datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S.%f')

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
    date_time_string = ts.getTimestampString() # a.k.a get the timestamp from the databse
    date_time_obj = ts.stringToTimestamp(date_time_string) # create a datetime data object from the timestamp string

    ts.printTimestamp(date_time_obj) # parse and print the timedate data object

if __name__ == "__main__":
    main()
