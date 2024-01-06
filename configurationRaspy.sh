#!/bin/bash

#git clone https://github.com/gabrielemrt/trackingService.git

sudo apt-get install figlet -y
sudo apt-get install vim -y

figlet "UPDATE & UPGRADE"
sudo apt update 
sudo apt upgrade -y

figlet "SET MULTI-USER.TARGET"
sudo systemctl set-default multi-user.target


figlet "CONFIGURATION ETH0"
echo "interface eth0" >> /etc/dhcpcd.conf
echo "static ip_address=192.168.2.XX/24" >> /etc/dhcpcd.conf
#echo "#static ip6_address=fd51:42f8:caae:d92e::ff/64" >> /etc/dhcpcd.conf
echo "static routers=192.168.2.2" >> /etc/dhcpcd.conf
echo "static domain_name_servers=192.168.2.2 8.8.8.8" >> /etc/dhcpcd.conf

figlet "CONFIGURATION WLAN0"
echo "interface wlan0" >> /etc/dhcpcd.conf
echo "static ip_address=192.168.2.XX/24" >> /etc/dhcpcd.conf
#echo "#static ip6_address=fd51:42f8:caae:d92e::ff/64" >> /etc/dhcpcd.conf
echo "static routers=192.168.2.2" >> /etc/dhcpcd.conf
echo "static domain_name_servers=192.168.2.2 8.8.8.8" >> /etc/dhcpcd.conf
