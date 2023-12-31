#!/bin/bash -i
sudo -i
apt-get update && apt-get -y install libncurses5
apt-get -y install sysbench

#Install sakila
mkdir /home/sakila
cd /home/sakila
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xvzf sakila-db.tar.gz
#Sakila config
mysql -Bse "SOURCE /home/sakila/sakila-db/sakila-schema.sql;SOURCE /home/sakila/sakila-db/sakila-data.sql;"

# install mysql-cluster
mkdir -p /opt/mysqlcluster/home
wget -P /opt/mysqlcluster/home http://dev.mysql.com/get/Downloads/MySQL-Cluster-7.2/mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
tar xvf /opt/mysqlcluster/home/mysql-cluster-gpl-7.2.1-linux2.6-x86_64.tar.gz
ln -s /opt/mysqlcluster/home/mysql-cluster-gpl-7.2.1-linux2.6-x86_64 mysqlc
echo 'export MYSQLC_HOME=/opt/mysqlcluster/home/mysqlc' > /etc/profile.d/mysqlc.sh
echo 'export PATH=$MYSQLC_HOME/bin:$PATH' >> /etc/profile.d/mysqlc.sh
source /etc/profile.d/mysqlc.sh
mkdir -p /opt/mysqlcluster/deploy
mkdir /opt/mysqlcluster/deploy/conf
mkdir /opt/mysqlcluster/deploy/mysqld_data
mkdir /opt/mysqlcluster/deploy/ndb_data

# Setup Masetr node config
cat <<EOF > /opt/mysqlcluster/deploy/conf/my.cnf
[mysqld]
ndbcluster
datadir=/opt/mysqlcluster/deploy/mysqld_data
basedir=/opt/mysqlcluster/home/mysqlc
port=3306
EOF


