#!/bin/bash -i

sudo -i
# Setup Masetr node config
cat <<EOF > /opt/mysqlcluster/deploy/conf/my.cnf
[ndbd default]
# Options affecting ndbd processes on all data nodes:
NoOfReplicas=3	# Number of replicas
datadir=/opt/mysqlcluster/deploy/ndb_data

[ndb_mgmd]
# Management process options:
hostname= $1 # Hostname of the manager
datadir=/opt/mysqlcluster/deploy/ndb_data     # Directory for the log files
NodeId=1

[ndbd]
hostname= $2 # Hostname/IP of the first data node
NodeId=2			# Node ID for this data node
datadir=/opt/mysqlcluster/deploy/ndb_data 	# Remote directory for the data files

[ndbd]
hostname= $3 # Hostname/IP of the second data node
NodeId=3			# Node ID for this data node
datadir=/opt/mysqlcluster/deploy/ndb_data 	# Remote directory for the data files

[ndbd]
hostname= $4 # Hostname/IP of the second data node
NodeId=4			# Node ID for this data node
datadir=/opt/mysqlcluster/deploy/ndb_data 	# Remote directory for the data files

[mysqld]
# SQL node options:
NodeId=50

EOF



cd /opt/mysqlcluster/home/mysqlc
scripts/mysql_install_db –no-defaults –datadir=/opt/mysqlcluster/deploy/mysqld_data

/opt/mysqlcluster/home/mysqlc/bin/ndb_mgmd -f /opt/mysqlcluster/deploy/conf/config.ini --initial --configdir=/opt/mysqlcluster/deploy/conf/
/opt/mysqlcluster/home/mysqlc/bin/ndb_mgm -e show
mysqld –defaults-file=/opt/mysqlcluster/deploy/conf/my.cnf –user=root &

/opt/mysqlcluster/home/mysqlc/bin/ndb_mgm -e show
mysql_secure_installation

#Create a user
mysql -Bse "CREATE USER 'myapp'@'%';GRANT ALL ON *.* TO 'myapp'@'%';"
#Flush restrictions
mysql -Bse "FLUSH PRIVILEGES;FLUSH TABLES WITH READ LOCK;UNLOCK TABLES;"
