#!/bin/bash -i
sudo -i
mkdir -p /opt/mysqlcluster/deploy/ndb_data
/opt/mysqlcluster/home/mysqlc/bin/ndbd -c $1