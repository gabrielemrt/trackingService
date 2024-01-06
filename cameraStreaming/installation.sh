#!/bin/bash

## INSTALLAZIONE DEL SERVIZIO DI STREAMING
figlet "INSTALLATION SERVER STREAMING"
sudo apt-get update
sudo apt-get install mjpg-streamer -y


## AVVIO IL SERVIZIO DI STREAMING
figlet "START STREAMING SERVICE"
mjpg_streamer -i "input_raspicam.so" -o "output_http.so -p 8080"



## 1. Install system dependencies:
sudo apt-get update && sudo apt-get install -y python3-dev libjpeg-dev libatlas-base-dev raspi-gpio libhdf5-dev python3-smbus

## 2. Create a new project directory:
mkdir rpi-deep-pantilt && cd rpi-deep-pantilt

## 3. Create a new virtual environment:
python3 -m venv .venv

## 4. Activate the virtual environment:
source .venv/bin/activate && python3 -m pip install --upgrade pip

## 5. Install TensorFlow 2.0 from a community-built wheel:
pip install https://github.com/leigh-johnson/Tensorflow-bin/blob/master/tensorflow-2.0.0-cp37-cp37m-linux_armv7l.whl?raw=true

## 6. Install the rpi-deep-pantilt Python package:
python3 -m pip install rpi-deep-pantilt
