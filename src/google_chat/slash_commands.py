import json
import re
from log import Logger
from google_chat.ip_release import ip_release_handler
LOGGER = Logger()

def slash_command_handler(event, user_name):
    text = validate_commands(event, user_name)
    return text

def validate_commands(event, user_name):
    commandId = event['message']['slashCommand']['commandId']
    args = event['message']['argumentText'].replace(' ', '', 1).split()
    if commandId == "1":
        nargs = 1
        if validate_args(args, nargs):
            publicIp = args[0]
            if validate_ip(args):
                LOGGER.info(f'Valid Ip address -> {publicIp}')
                text = ip_release_handler(publicIp, user_name)
                return text
            else:
                text = 'Invalid Ip address'
                LOGGER.error(text)
                return text
        else:
            text = f'Incorrect number of arguments, this command accepts only {nargs} arguments'
            LOGGER.error(text)
            return text

def validate_ip(args):
    # for validating an Ip-address 
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex, args[0])):
        return True
    else:
        return False

def validate_args(args, nargs):
    if len(args) == nargs:
        return True
    else:
        return False
