import os
import re
import json
from datetime import datetime
from aws_waf.update_ipset import update_ipset_handler
from aws_waf.clean_ipset import clean_ipset_handler
from google_chat.admin_auth import admin_authorization
from log import Logger

LOGGER = Logger()

GLOBAL_IPSET_DYNAMIC = os.getenv('GLOBAL_IPSET_DYNAMIC')
GLOBAL_IPSET_FIXED = os.getenv('GLOBAL_IPSET_FIXED')
REGIONAL_IPSET_DYNAMIC = os.getenv('REGIONAL_IPSET_DYNAMIC')
REGIONAL_IPSET_FIXED = os.getenv('REGIONAL_IPSET_FIXED')

def ip_release_handler(args, user_name, user_email):
    if validate_ip(args[0]):
        return dynamic_ip_handler(args[0], user_name, user_email)
    elif args[0] == 'dynamic' and validate_ip(args[1]):            
        return dynamic_ip_handler(args[1], user_name, user_email)
    elif args[0] == 'fixed' and validate_ip(args[1]):
        return fixed_ip_handler(args[1], user_name, user_email)
    elif args[0] == 'clean':
        return clean_ips(user_name, user_email)
    else:
        text = 'Invalid arguments\n\nThis command will accept only the following arguments:\n\n> /iprelease {publicIp}\n> /iprelease dynamic {publicIp}\n> /iprelease fixed {publicIp}'
        LOGGER.error(f'Invalid arguments: {args}')
        return text

def dynamic_ip_handler(publicIp, user_name, user_email):
    publicIp = [publicIp+'/32']
    text = update_ipset_handler(GLOBAL_IPSET_DYNAMIC, REGIONAL_IPSET_DYNAMIC, publicIp, user_name, action = 'INSERT')
    print(data_log(publicIp, user_name, user_email, type = 'dynamic'))
    return text

def fixed_ip_handler(publicIp, user_name, user_email):
    if admin_authorization(user_name, user_email):
        publicIp = [publicIp+'/32']
        text = update_ipset_handler(GLOBAL_IPSET_FIXED, REGIONAL_IPSET_DYNAMIC, publicIp, user_name, action = 'INSERT')
        print(data_log(publicIp, user_name, user_email, type = 'fixed'))
        return text
    else:
        return f'{user_name}, you are not authorized to execute this command, please contact your administrators'

def clean_ips(user_name, user_email):
    if admin_authorization(user_name, user_email):
        global_ips, regional_ips = clean_ipset_handler(GLOBAL_IPSET_DYNAMIC, REGIONAL_IPSET_DYNAMIC, user_name)
        print(data_log(global_ips, user_name, user_email, type = 'clean-global'))
        print(data_log(regional_ips, user_name, user_email, type = 'clean-regional'))
        return f"Dynamic ips have been cleaned"

def data_log(publicIp, user_name, user_email, type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps({
        "user_name": f"{user_name}",
        "email": f"{user_email}",
        "type": f"{type}",
        "publicIp": publicIp,
        "timestamp": f"{timestamp}"
    })

def validate_ip(publicIp):
    # for validating an Ip-address 
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex, publicIp)):
        LOGGER.info(f'Valid Ip address: {publicIp}')
        return True
    else:
        return False
