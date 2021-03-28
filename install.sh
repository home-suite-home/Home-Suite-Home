#!/bin/sh



# install mongodb
#starting the database
DB="mongodb-org"
if ! dpkg -s $DB > /dev/null 2>&1
then
    sudo apt-get install -y mongodb
fi
# update libraries
sudo apt-get update

# python3 just in case and firefox for UI just in case
sudo apt-get install python3 firefox

# get pip
sudo apt-get -y install python3-pip

# install python libraries
pip3 install pymongo
pip3 install dash
pip3 install dash_daq
pip3 install kaleido
