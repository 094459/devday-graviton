#!/bin/sh

echo "Install jq"
sudo yum install -y jq

echo "Installing git, compiler, depends..."
sudo yum install -y git
sudo yum -y install git gcc make automake libtool openssl-devel ncurses-compat-libs

echo "Installing MySQL Client"
sudo yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
sudo yum install -y mysql-community-client
sudo yum -y install mysql-community-devel mysql-community-client mysql-community-common

#<add apache ab >

echo "install load tools"

sudo amazon-linux-extras install epel -y
yum install -y stress
yum install -y httpd-tools

echo "install JMeter"

sudo yum install -y java-11-amazon-corretto
wget https://mirrors.ukfast.co.uk/sites/ftp.apache.org//jmeter/binaries/apache-jmeter-5.4.1.zip
unzip apache-jmeter-5.4.1.zip
rm apache-jmeter-5.4.1.zip

echo "compile sysbench"

git clone https://github.com/akopytov/sysbench
cd sysbench
./autogen.sh
./configure
make
sudo make install

curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.rpm.sh | sudo bash
sudo yum -y install sysbench

echo "Install python"
sudo yum install -y python3-pip


