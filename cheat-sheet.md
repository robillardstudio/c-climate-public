# Critical Climate Machine – Cheat-Sheet

Content:

- Python dependencies
- Import export MongoDB
- MongoDB Raspberry install
- BASH commands on Pi0
- BASH commands on Pi4
- Pi4 autostart
- Pi4 avoid sleep

## Python dependencies

* scikit-learn  
* numpy  
* pymongo  
* pymongo[srv]
* pickle

## Import export MongoDB

Local DB

export database:  
`mongoexport --collection=tweets --db=tweet-database --out=C:\Mypath\tweets.json`

import database:  
`mongoimport --db tweet-database --collection tweets --drop --file C:\Mypath\tweets.json`

Cloud DB

export  
`mongoexport --uri mongodb+srv://user:tweet@cluster0.pxkga.mongodb.net/tweet-database --collection tweets --out C:\Mypath\tweets.json`

import  
`mongoimport --uri mongodb+srv://user:tweet@cluster0.pxkga.mongodb.net/tweet-database --collection tweets --drop --file C:\Mypath\tweets.json`

if DB is transfered locally on Pi4...

with  
-d localtweetdb (database)  
-c tweets (collection)

import json  
`mongoimport /home/pi/Downloads/tweets.json -d localtweetdb -c tweets --drop --jsonArray`

to communicate with pi4 db from python code, use pip3 install pymongo==3.4.0

## MongoDB Raspberry install

from https://www.mongodb.com/developer/how-to/mongodb-on-raspberry-pi/

instead of `sudo apt-get install -y mongodb-org`

use `sudo apt-get install -y mongodb`

then

### Ensure mongod config is picked up:
`sudo systemctl daemon-reload`

### Tell systemd to run mongod on reboot:
`sudo systemctl enable mongodb`

### Start up mongod!
`sudo systemctl start mongodb`

check if service is running correctly: `sudo systemctl status mongodb`

should return

```
● mongod.service - MongoDB Database Server
   Loaded: loaded (/lib/systemd/system/mongod.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2020-08-09 08:09:07 UTC; 4s ago
   Docs: https://docs.mongodb.org/manual
Main PID: 2366 (mongod)
   CGroup: /system.slice/mongod.service
         └─2366 /usr/bin/mongod --config /etc/mongod.conf
```

## BASH commands on Pi0

Kill Python script

`pkill -f name-of-the-python-script`

Download files from SMB server (the folder must be set as shared folder on the server)

`smbget -R -D -u -n smb://pi:wave@192.168.1.200/c-climate`

Launch server

`Server/server.launch`

To uninstall and reinstall last version of numpy

```
sudo apt update
sudo apt remove python3-numpy
sudo apt install libatlas3-base
sudo pip3 install numpy
```
To check space left on the disk

`df -BM`

To execute the bashrc

`source ~/.bashrc`

## BASH commands on On Pi4

### Configure samba shared folder

Samba should be installed

Set your share folders. Do something like this (change your path and comments)

```
[MyShare]
  comment = YOUR COMMENTS
  path = /your-share-folder
  read only = no
  guest ok = yes
```
Restart samba. type: `/etc/init.d/smbd restart`

If needed check if folder's permissions are set.

## Pi4 autostart

in .config/autostart edit scenario.desktop

```
[Desktop Entry]
Type=Application
Name=Scenario
Exec=/home/pi/c-climate/start.sh
```

```
Exec=/home/pi/Downloads/HeatMapV1/application.linux-armv6hf/HeatMapV1
```

# Pi4 avoid sleep

edit lightdm.conf

`sudo nano /etc/lightdm/lightdm.conf`

add this line at the end of the file

[SeatDefaults]
xserver-command=X -s 0 -p 0 -dpms
