#!/bin/bash

# Update package list
sudo apt-get update -y
apt-get update && apt-get -y install libncurses5
apt-get -y install sysbench


# Install MySQL Server without interactive prompts
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server

# Start MySQL service
sudo service mysql start

sudo wget https://downloads.mysql.com/docs/sakila-db.tar.gz
dpkg -i sakila-db.tar.gz



