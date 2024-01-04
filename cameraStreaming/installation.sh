#!/bin/bash

## INSTALLAZIONE DEL SERVIZIO DI STREAMING
figlet "INSTALLATION SERVER STREAMING"
sudo apt-get update
sudo apt-get install mjpg-streamer -y


## AVVIO IL SERVIZIO DI STREAMING
figlet "START STREAMING SERVICE"
mjpg_streamer -i "input_raspicam.so" -o "output_http.so -p 8080"
