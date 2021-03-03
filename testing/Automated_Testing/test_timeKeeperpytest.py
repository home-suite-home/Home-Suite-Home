# Automated test for timeKeeper.py
import datetime 
import pytest
from timeKeeper import TimeStamps 

# testing the stringToTimeStamp function
def test_stringToTimestamp():
    timeStamp = TimeStamps.stringToTimestamp(TimeStamps,"2021-03-03 18:09:19.611086")
    assert (timeStamp.strftime("%Y") == "2021")
    assert (timeStamp.strftime("%m") == "03")
    assert (timeStamp.strftime("%d") == "03")
    assert (timeStamp.strftime("%H") == "18")
    assert (timeStamp.strftime("%M") == "09")
    assert (timeStamp.strftime("%S.%f") == "19.611086")

