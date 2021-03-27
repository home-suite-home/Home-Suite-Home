#!/bin/sh

# update libraries
sudo apt-get update

# python3 just in case and firefox for UI just in case
sudo apt-get install python3 firefox

# get pip
sudo apt-get -y install python3-pip

# install mongodb
#starting the database
DB="mongodb"
if ! dpkg -s $DB > /dev/null 2>&1
then
    sudo apt install -y mongodb
fi

# install python libraries
pip3 install pymongo
pip3 install dash
pip3 install dash_daq
pip3 install kaleido
