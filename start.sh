#!/bin/bash
#
#

# Start script to begin scenario

sleep 10

# puredata /home/pi/Wavematrix-scenario/main.pd

cd /home/pi/c-climate/claim_monitor

lxterminal -e python3 cl_monitor.py &

sleep 30

cd /home/pi/c-climate

lxterminal -e python3 scenario.py &


