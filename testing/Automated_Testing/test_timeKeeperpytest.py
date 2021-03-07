#
#   Filename: test_timeKeeperpytest.py
#   Date: 03/06/2021
#
#   Engineer: Andres Graterol
#   Contact: graterol.andres0@knights.ucf.edu
#
#   Description: Automated Unit test for timeKeeper.py
#                Grabs a string from getTimeStamp()
#                Tests the individual aspects of stringToTimestamp()
#

# Automated test for timeKeeper.py
import datetime
import pytest
from timeKeeper import TimeStamps

# testing the stringToTimeStamp function


def test_stringToTimestamp():
    # 1615082379 is an int pulled from .getTimeStamp
    timeStamp = TimeStamps.stringToTimestamp(TimeStamps, 1615082379)

    # Showing the timestamp that we just passed
    TimeStamps.printTimestamp(TimeStamps, timeStamp)

    # asserting the year...
    assert (timeStamp.strftime("%Y") == "2021")
    # the month...
    assert (timeStamp.strftime("%m") == "03")
    # the day...
    assert (timeStamp.strftime("%d") == "06")
    # the hour...
    assert (timeStamp.strftime("%H") == "20")
    # the minute...
    assert (timeStamp.strftime("%M") == "59")
    # the second...
    assert (timeStamp.strftime("%S.%f") == "39.000000")
