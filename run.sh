#!/bin/sh

# kill all processes on exit
trap 'echo Killing Home-Suite-Home ...;  kill $(pgrep -f 'sensor_driver.py'); kill $(pgrep -f 'EmailCommandDriver.py'); kill $(pgrep -f 'User_Interface.py'); sudo systemctl stop mongodb; exit' INT TERM

echo "Starting Home-Suite-Home ..."
echo "CTRL-C to quit"

# start the database
sudo systemctl start mongodb

# move to source directory
cd source

# start Driver processes
python3 sensor_driver.py &
python3 EmailCommandDriver.py &
python3 User_Interface.py &

# open the UI window
echo "If User Interface page does not connect: wait a second and hit refresh"
sleep 3
file="tmp.txt"
addr=$(cat "$file")
firefox $addr

wait
