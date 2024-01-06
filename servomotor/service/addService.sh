#!/bin/bash

sudo cp ./servomotor.service /etc/systemd/system/

sudo systemctl enable servomotor.service 
sudo systemctl start servomotor.service 

sudo systemctl status mio_servizio.service
