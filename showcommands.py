#!/usr/bin/env python3

from netmiko import ConnectHandler
import yaml
from pprint import pprint

# OPEN THE FILE OF NETMIKO DETAILS AND SAVE THEM IN VARIABLE NAMED TARGETS.
with open('/mnt/c/Users/Stephen Hendry/PycharmProjects/netmiko/targets.yaml', 'r') as details:
    targets = yaml.load(details, Loader=yaml.FullLoader)

#CREATE LIST OF COMMANDS WHICH WILL BE SENT TO DEVICES
show_commands = ['show cdp neighbors detail']


#CREATE A LOOP WHICH WILL UNPACK THE VALUES OF ['ALL_DEVICES'] KEY IN TARGETS VARIABLE.
#THIS CREATES TWO VARIABLES - DEVICE (TYPE: STRING, CONTAINS: NAME OF DEVICE) AND
#CONFIG (TYPE: DICT, CONTAINS: NETMIKO CONNECTION DETAILS)
for device, config in targets['all_devices'].items():
    print('#' * 25 + 'CONNECTING TO ' + device.upper() + '#' * 25)
    #PASS NETMIKO CONNECTION DETAILS OF NETMIKO 'CONNECTHANDLER'
    net_connect = ConnectHandler(**config)
    #CREATE ANOTHER LOOP, NESTED WITHIN PREVIOUS LOOP WHICH WILL ITERATE OVER COMMANDS STORED IN
    #SHOW_COMMANDS VARIABLE.
    for command in show_commands:
        print('#' * 25 + 'OUTPUT FROM ' + command.upper() + ' ON ' + device.upper() + '#' * 25)
        #SEND COMMAND TO DEVICE AND PRINT RESPONSE
        sent_commands = net_connect.send_command(command, use_genie=True)
        pprint(sent_commands)














