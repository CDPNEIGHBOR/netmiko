#!/usr/bin/env python3

from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko import ConnectHandler
from jinja2 import FileSystemLoader, Environment
import yaml

#OPEN THE FILE OF NETMIKO DETAILS AND SAVE THEM IN VARIABLE NAMED TARGETS.
with open('/mnt/c/Users/Stephen Hendry/PycharmProjects/netmiko/targets.yaml', 'r') as details:
    targets = yaml.load(details, Loader=yaml.FullLoader)

# OPEN THE FILE OF TOPOLOGY DETAILS AND SAVE THEM IN A VARIABLE NAMED CONFIGURATION
with open('/mnt/c/Users/Stephen Hendry/PycharmProjects/netmiko/topology.yaml', 'r') as topology:
    configuration = yaml.load(topology, Loader=yaml.FullLoader)


#SPECIFY DEVICES WITHIN THE TOPOLOGY.YAML FILE THAT WILL BE TEMPLATED
topology_data = configuration['all_devices']

# SPECIFY THE DIRECTORY WHERE THE TEMPLATE ITSELF IS STORED
template_dir = "/mnt/c/Users/Stephen Hendry/PycharmProjects/netmiko"

# SPECIFY TEMPLATE JINJA ENVIRONMENT PARAMETERS.
template_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)


#THIS FUNCTION USES JINJA2 TEMPLATE AND TOPOLOGY.YAML FILE TO CREATE TEMPLATE FROM WHICH
# A LIST OF COMMANDS CAN BE GENERATED.
def make_template():
    for device, config in targets['all_devices'].items():
        print('#' * 25 + 'RENDERING TEMPLATE FOR ' + device.upper() + '#' * 25)
        base_template = template_env.get_template('topology.j2')
        render = base_template.render(topology_data[device])
        #RENDERING JINJA TEMPLATE YIELDS A STRING. THIS MAY CAUSE ISSUES AS
        #STRINGS CAN BE SENT TO NETMIKO BUT WILL CAUSE TIMEOUTS FOR LONG INPUTS
        #USE SPLITLINES TO CREATE LIST FROM 'RENDER' VARIABLE.
        commands = render.splitlines()
        #BLANK LINES IN RENDERED JINJA TEMPLATE WILL YIELD BLANK ENTRY ("") IN LIST CREATED BY
        #SPLITLINES. WHILE LOOP REMOVES THESE TO REDUCE UNNECESSARY INPUT.
        while "" in commands:
            commands.remove("")
        #CALL FUNCTION WHICH WILL INITIATE NETMIKO CONNECTION AND PASS IT REQUIRED ARGS AS FOLLOWS
        #DEVICE (TYPE: STRING, CONTAINS: DEVICE NAME - FOR COHERENCE), CONFIG (TYPE: DICT, CONTAINS: NETMIKO
        #CONNECTION PARAMETERS) AND COMMANDS (TYPE: LIST, CONTAINS: COMMANDS GENERATED FROM JINJA TEMPLATE)
        send_template(device, config, commands)


#DEFINE FUNCTION TO SEND TEMPLATES TO DEVICES, INCLUDING THE PARAMETERS PASSED FROM PREVIOUS FUNCTION.
def send_template(device, config, commands):
    print('#' * 25 + 'CONNECTING TO ' + device.upper() + '#' * 25)
    try:
        #FOR EACH CONNECT HANDLER IS PASSED DEVICE SPECIFIC 'CONFIG' (TYPE: DICT CONTAINS: CONNECTION PARAMETERS)
        net_connect = ConnectHandler(**config)
        #PASS COMMANDS (TYPE: LIST, CONTAINS: LIST OF COMMANDS FROM JINJA TEMPLATE) TO SEND_CONFIG_SET
        sent_commands = net_connect.send_config_set(commands)
        #PRINTING SENT_COMMANDS RETURNS OUTPUT OF CLI AS WOULD BE SEEN IF THE DEVICE WERE BEING CONFIGURED
        #IN PERSON.
        print(sent_commands)
        #USE EXCEPTION HANDLING TO CATCH ANY POSSIBLE TIMEOUT EXCEPTIONS
    except NetMikoTimeoutException:
        print("Timeout exception raised on " + device.upper())


make_template()
