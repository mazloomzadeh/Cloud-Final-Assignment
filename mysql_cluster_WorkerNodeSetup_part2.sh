#!/bin/bash -i
sudo -i
mkdir -p /opt/mysqlcluster/deploy/ndb_data
ndbd -c $1