#!/bin/sh

trap goaway INT TERM HUP

goaway()
{
    echo ""
    echo "Shutting down Home-Suite-Home ..."
    echo ""
    echo "stopping database process"
    sudo systemctl stop $DB

    echo "stopping user interface: Please close browser window"
    kill $(pgrep -f  'User_Interface.py') > /dev/null 2>&1

    echo "stopping sensor driver"
    kill $(pgrep -f  'sensor_driver.py') > /dev/null 2>&1

    echo "stopping email driver"
    kill $(pgrep -f  'EmailCommandDriver.py') > /dev/null 2>&1

    rm -f $file

    # gives the terminal back control
    stty sane

    exit
}

dead_child()
{
    echo ""
    echo "Process $1 has failed: Shutting down"
    echo ""
    echo "Press Enter twice after shutdown to return to normal terminal"
    echo ""
    goaway
}

echo "Starting Home-Suite-Home ..."
echo "[CTRL-C to quit]"
echo ""

#starting the database
DB="mongodb-org"
if dpkg -s $DB > /dev/null 2>&1
then
    DB="mongodb"
else
    DB="mongod"
fi
echo "Starting $DB ..."
sudo systemctl start $DB
sudo systemctl status $DB &

# Moving to source directory
cd source

# Start Driver Processes and catch errors
python3 User_Interface.py &
if $? > /dev/null 2>&1
then
    ARG="User_Interface.py"
    dead_child $ARG
fi

python3 sensor_driver.py &
if $? > /dev/null 2>&1
then
    ARG="sensor_driver.py"
    dead_child $ARG
fi

python3 EmailCommandDriver.py &
if $? > /dev/null 2>&1
then
    ARG="EmailCommandHandler.py"
    dead_child $ARG
fi

sleep 3
file="tmp.txt"
addr=$(cat "$file")
firefox $addr

# check for dead children
while true
do
    if ! pgrep -f 'User_Interface.py' > /dev/null 2>&1
        then
        ARG="User_Interface.py"
        dead_child $ARG
    fi

    if ! pgrep -f 'sensor_driver.py' > /dev/null 2>&1
        then
        ARG="sensor_driver.py"
        dead_child $ARG
    fi

    if ! pgrep -f 'EmailCommandDriver.py' > /dev/null 2>&1
        then
        ARG="EmailCommandDriver.py"
        dead_child $ARG
    fi
done
