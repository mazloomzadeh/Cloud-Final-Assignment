#!/bin/bash

apt-get update

#Install needed dependencies
apt-get install python3 python3-pip -y

pip3 install flask 
pip3 install flask-restful