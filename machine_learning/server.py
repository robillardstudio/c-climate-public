'''Simplified BSD License

Copyright (c) 2021 Gaëtan Robillard and Jolan Goulin

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.'''

# PI ZERO SERVER
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

import argparse
import math
import os
import os.path
import sys
import time
from time import sleep
from time import ctime
import subprocess
import socket
import utils as u
from ml import ml_logistic

# Setup the max7219 device
# ----------------------------------------------------------------------
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

serial = spi(port=0, device=0, gpio=noop(), bus_speed_hz=500000)
device = max7219(serial, cascaded=7, blocks_arranged_in_reverse_order=True)
seg = sevensegment(device)

# Import the OSC-library
# ----------------------------------------------------------------------
from pythonosc import dispatcher
from pythonosc import osc_server

Hostname = subprocess.check_output("hostname | tr -d \" \t\n\r\"", shell=True).decode("utf-8")
cmd = "vcgencmd measure_temp | sed s/[^0-9.]//g | sed 's/\..*$//'"

print(Hostname)

ips = subprocess.check_output(['hostname', '--all-ip-addresses'])
my_ip = ips.decode('utf-8')
this_ip = my_ip[:13]

print("this_ip",this_ip)

# Parse the arguments from command-line
# ----------------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument("--ip",
    default="127.0.0.1", help="The ip to listen on")
parser.add_argument("--port",
    type=int, default=5005, help="The port to listen on")

args = parser.parse_args()

# Few variables
#-----------------------------------------------------------------------
tweet_list = []

# Define the functions
# ----------------------------------------------------------------------
def simple_message(unused_addr,the_message):
  try:
    print("receiving simple message")
    seg.text = "{}".format(the_message)
  except ValueError: pass
    
def tweet(unused_addr,tweet):
  try:
    numer = [ord(c) for c in tweet]
    str1 = [str(x) for x in numer]
    str2 = ''.join(str1)
    sentence = str2.replace("0", "")
    seg.text = "{}".format(sentence[0:55])
    tweet_list.append(tweet)
    # ~ print("tweet_list length:",len(tweet_list))
    if (len(tweet_list) == 28):
        print("tweet_list is complete")
  except ValueError: pass
  
def flush(unused_addr,value):
  try:
    if (value):
      tweet_list.clear()
      print("cleared; length:",len(tweet_list))
  except ValueError: pass
    
def ml_process(unused_addr,value):
  try:
    if (value):
      result = ml_logistic(tweet_list)
      # ~ print(result)
      display = clean2text(result)
      print(display)
      seg.text = "{}".format(display[0:55])
  except ValueError: pass
  
# Utilities
# ----------------------------------------------------------------------
def clean2text(values):
  formated = []
  for i in range(len(values)):
    formated.append(f"{values[i]:02d}")
  str1 = ''.join(formated)
  sentence = str1.replace("0", "-")
  return sentence
  
def loc_update(unused_addr,value):
    try:
      if (value):
        print ("")
        print ("Local update ...")
        os.system("smbget -R -D -u -n smb://pi:wave@192.168.1.200/c-climate/machine_learning")
        print("OK")
        seg.text = "UPDATE OK"
    except ValueError: pass
    
def stop_system(unused_addr, value):
    try:
        os.system("sudo shutdown now")
    except ValueError: pass

def reboot(unused_addr, value):
    try:
        os.system("sudo shutdown -r now")
    except ValueError: pass

# Start the server-process
# ----------------------------------------------------------------------
if __name__ == "__main__":
  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/simple_message", simple_message)
  dispatcher.map("/flush", flush)
  dispatcher.map("/tweet", tweet)
  dispatcher.map("/ml_process", ml_process)
  dispatcher.map("/loc_update", loc_update)
  dispatcher.map("/stop_system", stop_system)
  dispatcher.map("/reboot", reboot)

  server = osc_server.ThreadingOSCUDPServer((this_ip, args.port), dispatcher)
  
  print("{} is serving on {}".format(Hostname, server.server_address))
  print("=============================================================")
  
  seg.text = "{:<8}{:<8}{:<8}{:<8}{:<8}".format("SERVER","IS","RUNNING","ML","LOADED")
  server.serve_forever()
