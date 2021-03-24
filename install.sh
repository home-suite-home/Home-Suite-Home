#!/bin/sh

# update libraries
sudo apt-get update

# get pip
sudo apt-get -y install python3-pip

# install mongodb
sudo apt install -y mongodb

# install python libraries
pip3 install pymongo
pip3 install dash
pip3 install dash_daq
pip3 install kaleido
