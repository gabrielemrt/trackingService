#!/bin/bash

### INSTALLAZIONE DEL SERVIZIO DI STREAMING
#figlet "INSTALLATION SERVER STREAMING"
#sudo apt-get update
#sudo snap install mjpg-streamer


## INSTALLAZIONE STRUMENTI SVILUPPATORE
figlet "INSTALLAZIONE STRUMENTI SVILUPPATORE"
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install build-essential cmake git pkg-config libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev gfortran openexr libatlas-base-dev python3-dev python3-numpy libtbb2 libtbb-dev libdc1394-22-dev -y


## INSTALLAZIONE PACCHETTI
figlet "INSTALLAZIONE PACCHETTI"
sudo pip3 install opencv-python
sudo pip3 install flask
sudo pip3 install flask-socketio
