#!/bin/bash -i

sudo -i

cd /install
cat <<EOF > /etc/mysql/my.cnf
[mysqld]
# Options for mysqld process:
ndbcluster                      # run NDB storage engine

[mysql_cluster]
# Options for NDB Cluster processes:
ndb-connectstring=$1 # location of management server
EOF

systemctl restart mysql
systemctl enable mysql
sudo -i

# Setup Masetr node config
cat <<EOF > /opt/mysqlcluster/deploy/conf/config.ini
ndbd default]
# Options affecting ndbd processes on all data nodes:
NoOfReplicas=3  # Number of replicas
datadir=/opt/mysqlcluster/deploy/ndb_data

[ndb_mgmd]
# Management process options:
hostname=$1
datadir=/opt/mysqlcluster/deploy/ndb_data
nodeid=1

[ndbd]
hostname=$2
nodeid=2
datadir=/opt/mysqlcluster/deploy/ndb_data

[ndbd]
hostname=$3
nodeid=3
datadir=/opt/mysqlcluster/deploy/ndb_data

[ndbd]
hostname=$4
nodeid=4
datadir=/opt/mysqlcluster/deploy/ndb_data

[mysqld]
nodeid=50

EOF

# cd /opt/mysqlcluster/home/mysqlc
# scripts/mysql_install_db –-no-defaults –-datadir=/opt/mysqlcluster/deploy/mysqld_data
/opt/mysqlcluster/home/mysqlc/scripts/mysql_install_db --no-defaults --datadir=/opt/mysqlcluster/deploy/mysqld_data

/opt/mysqlcluster/home/mysqlc/bin/ndb_mgmd -f /opt/mysqlcluster/deploy/conf/config.ini --initial --configdir=/opt/mysqlcluster/deploy/conf/ --ndb-nodeid=1

/opt/mysqlcluster/home/mysqlc/bin/ndb_mgm -e show
# /opt/mysqlcluster/home/mysqlc/bin/mysqld --defaults-file=/opt/mysqlcluster/deploy/conf/my.cnf -user=root &
/opt/mysqlcluster/home/mysqlc/bin/mysqld --defaults-file=/opt/mysqlcluster/deploy/conf/my.cnf --user=root &

/opt/mysqlcluster/home/mysqlc/bin/ndb_mgm -e show
/opt/mysqlcluster/home/mysqlc/bin/mysql/mysql_secure_installation

#Create a user
/install/mysql -Bse "CREATE USER 'myapp'@'%';GRANT ALL ON *.* TO 'myapp'@'%';"
#Flush restrictions
/install/mysql -Bse "FLUSH PRIVILEGES;FLUSH TABLES WITH READ LOCK;UNLOCK TABLES;"
