'''
CCM
Copyright (c) 2021 Gaëtan Robillard and Jolan Goulin
BSD Simplified License.
For information on usage and redistribution, and for a DISCLAIMER OF ALL
WARRANTIES, see the file, "LICENSE.txt," in this distribution.
'''

# Works on Ubuntu but only one core

import time
import datetime
import ml_upd_db as upd

while(True):
    CurrentTime = datetime.datetime.now()

    with open(r"/sys/class/thermal/thermal_zone0/temp") as File:
        CurrentTemp = File.readline()

    print(str(CurrentTime) + " - " + str(float(CurrentTemp) / 1000))

    time.sleep(1)

# Temperature monitor (to be used on raspberry)
# ------------------------------------------------------------------------------
def temp():
    cmd = "vcgencmd measure_temp | sed s/[^0-9.]//g | sed 's/\..*$//'"
    temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    print(temp)
    return temp

