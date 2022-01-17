# NETWORK MANAGEMENT
# ----------------------------------------------------------------------

import argparse
from pythonosc import udp_client

# Create a list of raspberry pi0 ip
# ----------------------------------------------------------------------
list_ip = []
for i in range(32):
    if (i>=9):
        list_ip.append("192.168.1.1"+ str(i+1))
    else :
        list_ip.append("192.168.1.10"+ str(i+1))
        
# Parsing argument
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,
    help="The port the OSC server is listening on")
args = parser.parse_args()

def update():
    print("updating...")
    for i in range(len(list_ip)):
        args.ip = list_ip[i]
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client.send_message("/loc_update",True)
    print("message passed")
    
def halt():
    print("stopping...")
    for i in range(len(list_ip)):
        args.ip = list_ip[i]
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client.send_message("/stop_system",True)
    print("message passed")
    
def reboot():
    print("rebooting...")
    for i in range(len(list_ip)):
        args.ip = list_ip[i]
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client.send_message("/reboot",True)
    print("message passed")

value = input("Please enter a command: ")

if (value == "update"):
    update()
    
if (value == "halt"):
    halt()
    
if (value == "reboot"):
    reboot()
    
    
    
