#!/bin/bash

curl --silent --location https://rpm.nodesource.com/setup_12.x | bash -
sudo yum install -y nodejs make gcc gcc-c++ tmux
sudo runuser -u ec2-user -- bash -c 'wget -O - https://d2j6vhu5uywtq3.cloudfront.net/static/c9-install.sh | bash'

export UNIX_USER="ec2-user"
export UNIX_USER_HOME="/home/ec2-user"
export ENVIRONMENT_PATH="/home/ec2-user/environment"
export UNIX_GROUP=$(id -g -n "$UNIX_USER")

echo "Installing environment"

sudo yum install -y aws-cfn-bootstrap
sudo mkdir /home/ec2-user/environment

echo "Install jq"
sudo yum install -y jq

echo "Installing git, compiler, depends..."

sudo yum install -y git
sudo yum -y install git gcc make automake libtool openssl-devel ncurses-compat-libs