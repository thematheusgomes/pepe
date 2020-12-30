import os
from ipaddress import ip_address
from aws_waf.update_ipset import update_ipset_handler
from aws_waf.clean_ipset import clean_ipset_handler
from aws_sg.security_group import security_group_handler
from google_chat.user_authorization import user_authorization
from log import Logger, data_log

LOGGER = Logger()

GLOBAL_IPSET_DYNAMIC = os.getenv('GLOBAL_IPSET_DYNAMIC')
GLOBAL_IPSET_FIXED = os.getenv('GLOBAL_IPSET_FIXED')
REGIONAL_IPSET_DYNAMIC = os.getenv('REGIONAL_IPSET_DYNAMIC')
REGIONAL_IPSET_FIXED = os.getenv('REGIONAL_IPSET_FIXED')

def ip_release_handler(args, user_name, user_email):
    if args[0] == 'dynamic' and validate_ip(args[1]):
        return dynamic_ip_handler(args[1], user_name, user_email)
    elif args[0] == 'fixed' and validate_ip(args[1]):
        return fixed_ip_handler(args[1], user_name, user_email)
    elif args[0] == 'clean':
        return clean_ips(user_name, user_email)
    elif args[0] == 'dev' or args[0] == 'qa' or args[0] == 'prod' or args[0] == 'tools' and validate_ip(args[1]):
        return security_group_handler(args[0], args[1], user_name, user_email)
    elif validate_ip(args[0]):
        return dynamic_ip_handler(args[0], user_name, user_email)
    else:
        text = 'Invalid arguments\n\nThis command will accept only the following arguments:\n\n> /iprelease {publicIp}\n> /iprelease dynamic {publicIp}\n> /iprelease fixed {publicIp}'
        LOGGER.error(f'Invalid arguments: {args}')
        return text

def dynamic_ip_handler(publicIp, user_name, user_email):
    publicIp = [publicIp+'/32']
    text = update_ipset_handler(GLOBAL_IPSET_DYNAMIC, REGIONAL_IPSET_DYNAMIC, publicIp, user_name, action = 'INSERT')
    print(data_log(publicIp, user_name, user_email, type = 'waf_dynamic'))
    return text

def fixed_ip_handler(publicIp, user_name, user_email):
    if user_authorization(user_name, user_email, type = 'admin'):
        publicIp = [publicIp+'/32']
        text = update_ipset_handler(GLOBAL_IPSET_FIXED, REGIONAL_IPSET_DYNAMIC, publicIp, user_name, action = 'INSERT')
        print(data_log(publicIp, user_name, user_email, type = 'waf_fixed'))
        return text
    else:
        return f'{user_name}, you are not authorized to execute this command, please contact your administrators'

def clean_ips(user_name, user_email):
    if user_authorization(user_name, user_email, type = 'admin'):
        global_ips, regional_ips = clean_ipset_handler(GLOBAL_IPSET_DYNAMIC, REGIONAL_IPSET_DYNAMIC, user_name)
        print(data_log(global_ips, user_name, user_email, type = 'clean-global'))
        print(data_log(regional_ips, user_name, user_email, type = 'clean-regional'))
        return f"Dynamic ips have been cleaned"

def validate_ip(publicIp):
    try:
        ip_address(publicIp)
        if ip_address(publicIp).is_private:
            LOGGER.error(f'The IP {publicIp} is private, the ip address must be public')
            return False
        else:
            LOGGER.info(f'Public IP address: {publicIp}')
            return True
    except Exception as e:
        LOGGER.error(e)
        return False
