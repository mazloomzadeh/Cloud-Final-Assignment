#!/bin/bash -i

apt-get update -y
apt-get -y install libncurses5

#Install mysql
apt-get install mysql-server -y

#install sakila
mkdir /home/sakila
cd /home/sakila
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xvzf sakila-db.tar.gz
#Sakila config : -B, --batch Don't use history file. Disable interactive behavior. starts with this option ENABLED by default! Disable with; -s, --silent Be more silent. Print results with a tab as separator, Buffer for TCP/IP and socket communication; -e, --execute=name Execute command and quit. (Disables --force and history file)
mysql -Bse "SOURCE /home/sakila/sakila-db/sakila-schema.sql;SOURCE /home/sakila/sakila-db/sakila-data.sql"

#Install sysbench
apt-get install sysbench -y



