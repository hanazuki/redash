#!/usr/bin/env bash

sudo apt-get -y update

# setup dependencies
# 1. python 2.7:
sudo apt-get install -y python-pip python-dev
sudo pip install --upgrade pip
# 2. redis
sudo apt-get install -y redis-server
# 3. PostgreSQL
sudo apt-get -y install postgresql-9.3 postgresql-server-dev-9.3
# 4. Node.js
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs build-essential
# git
sudo apt-get install -y git

# install some frontend tools globally
sudo npm install -g webpack
sudo npm install -g webpack-dev-server

cd /opt/redash/current
cp /opt/redash/current/setup/vagrant/files/env /opt/redash/current/.env
bower install

#install requirements
sudo pip install -r /opt/redash/current/requirements_dev.txt
sudo pip install -r /opt/redash/current/requirements.txt
sudo pip install pymongo==3.2.1

#create database
sudo -u postgres createuser vagrant --no-superuser --no-createdb --no-createrole
sudo -u postgres createdb redash --owner=vagrant
bin/run ./manage.py database create_tables
bin/run ./manage.py users create --admin --password admin "Admin" "admin"

#Purge Redis cache
redis-cli -n 1 FLUSHALL

#prepare client
cd /opt/redash/current/client
npm install
