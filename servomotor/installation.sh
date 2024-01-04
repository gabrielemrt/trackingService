#!/bin/bash

## INSTALLAZIONE PYTHON PER IL FUNZIONAMENTO DEL SERVIZIO
figlet "INSTALLATION PYTHON"
sudo apt-get update
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y

## INSTALLAZIONE DI FLASK (un framework web per Python per il controllo del servomotore)
figlet "INSTALLATION FLASK"
sudo pip3 install flask -y

## INSTALLAZIONE DI RPi.GPIO
figlet "INSTALLATION RPi.GPIO"
sudo apt-get install python3-rpi.gpio -y