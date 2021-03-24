#!/bin/sh

echo "Installing environment"

curl --silent --location https://rpm.nodesource.com/setup_12.x | bash -
yum install -y nodejs 
yum install -y make gcc gcc-c++ tmux
runuser -u ec2-user -- bash -c 'wget -O - https://d2j6vhu5uywtq3.cloudfront.net/static/c9-install.sh | bash'

export UNIX_USER="ec2-user"
export UNIX_USER_HOME="/home/ec2-user"
export ENVIRONMENT_PATH="/home/ec2-user/environment"
export UNIX_GROUP=$(id -g -n "$UNIX_USER")

yum install -y aws-cfn-bootstrap
yum install -y java-11-amazon-corretto
yum install -y jq
yum -y install git automake libtool openssl-devel ncurses-compat-libs

mkdir /home/ec2-user/environment
