#!/bin/sh

echo "**Install jq**"
sudo yum install -y jq

echo "**Installing git, compiler, depends...**"
sudo yum install -y git
sudo yum -y install git gcc make automake libtool openssl-devel ncurses-compat-libs

echo "Installing MySQL Client"
sudo yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
sudo yum install -y mysql-community-client
sudo yum -y install mysql-community-devel mysql-community-client mysql-community-common

echo "compile sysbench"
git clone https://github.com/akopytov/sysbench
cd sysbench
./autogen.sh
./configure
make
sudo make install

echo "Install python"
sudo yum install -y python3-pip

echo "Install Apache and PHP"

sudo usermod -a -G apache ec2-user
sudo chown -R ec2-user:apache /var/www
sudo chmod 2775 /var/www && find /var/www -type d -exec sudo chmod 2775 {} \;
find /var/www -type f -exec sudo chmod 0664 {} \;

sudo yum install -y httpd httpd-tools mod_ssl

sudo yum install amazon-linux-extras -y
sudo amazon-linux-extras enable php7.4
sudo yum clean metadata 
sudo yum install -y php php-common php-pear 
sudo yum install -y php-{cgi,curl,mbstring,gd,mysqlnd,gettext,json,xml,fpm,intl,zip} 

echo "<?php phpinfo(); ?>" > info.php
sudo mv info.php /var/www/html/

echo "Install MyPHPAdmin"

cd /var/www/html
wget https://www.phpmyadmin.net/downloads/phpMyAdmin-latest-all-languages.tar.gz
mkdir phpMyAdmin && tar -xvzf phpMyAdmin-latest-all-languages.tar.gz -C phpMyAdmin --strip-components 1
rm phpMyAdmin-latest-all-languages.tar.gz

echo "**Install PHP Benchmark**"

cd
git clone https://github.com/mysqlonarm/benchmark-suites
git clone https://github.com/vanilla-php/benchmark-php.git
cd benchmark-php
sudo mv benchmark.php /var/www/html/

echo "**Start Web Server**"

sudo systemctl start httpd 


