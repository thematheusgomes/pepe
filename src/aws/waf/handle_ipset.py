import os
from src.aws.waf.update_ipset import update_ipset
from src.aws.waf.clean_ipset import clean_ipset
from src.security.user_authorization import user_authorization

GLOBAL_IPSET_DYNAMIC = os.getenv('GLOBAL_IPSET_DYNAMIC')
GLOBAL_IPSET_FIXED = os.getenv('GLOBAL_IPSET_FIXED')
REGIONAL_IPSET_DYNAMIC = os.getenv('REGIONAL_IPSET_DYNAMIC')
REGIONAL_IPSET_FIXED = os.getenv('REGIONAL_IPSET_FIXED')

def dynamic_ip_handler(ipv, user_name, user_email):
    message = update_ipset(GLOBAL_IPSET_DYNAMIC, REGIONAL_IPSET_DYNAMIC, ipv, user_name, action='INSERT')
    return message

def fixed_ip_handler(ipv, user_name, user_email):
    if user_authorization(user_name, user_email, type='admin'):
        message = update_ipset(GLOBAL_IPSET_FIXED, REGIONAL_IPSET_FIXED, ipv, user_name, action='INSERT')
        return message
    return f'{user_name}, you are not authorized to execute this command, please contact your administrators'

def clean_ips_handler(user_name, user_email):
    if user_authorization(user_name, user_email, type = 'admin'):
        clean_ipset(GLOBAL_IPSET_DYNAMIC, REGIONAL_IPSET_DYNAMIC, user_name)
        return f"All dynamic ips have been removed"
    return f'{user_name}, you are not authorized to execute this command, please contact your administrators'
