#!/bin/bash -i

apt-get update -y
apt-get -y install libncurses5

#Install mysql
apt-get -y install mysql-server

#install sakila
mkdir /home/sakila
wget -P /home/sakila https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xvzf /home/sakila/sakila-db.tar.gz
#Sakila config
mysql -Bse "SOURCE /home/sakila/sakila-db/sakila-schema.sql;SOURCE /home/sakila/sakila-db/sakila-data.sql;"

#Install sysbench
apt-get -y install sysbench



