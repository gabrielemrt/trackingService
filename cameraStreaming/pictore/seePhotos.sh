#!/bin/bash

sudo apt update
sudo apt install snapd -y

sudo snap install core

sudo snap install imgcat


imgcat ./image.jpg
