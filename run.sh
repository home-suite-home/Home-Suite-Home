#!/bin/sh

# kill all processes on exit
trap 'kill $(pgrep -f 'sensor_driver.py');
       kill $(pgrep -f 'EmailCommandDriver.py');
       kill $(pgrep -f 'User_Interface.py');
       exit' INT TERM

echo "Starting Home-Suite-Home ..."
echo "CTRL-C to quit"

python3 source/sensor_driver.py &
python3 source/EmailCommandDriver.py &
python3 source/User_Interface.py &
