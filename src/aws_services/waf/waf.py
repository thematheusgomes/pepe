import os
from src.aws_services.waf.update_ipset import update_ipset
from src.aws_services.waf.clean_ipset import clean_ipset
from src.bot.user_authorization import user_authorization
from src.log import data_log

GLOBAL_IPSET_DYNAMIC = os.getenv('GLOBAL_IPSET_DYNAMIC')
GLOBAL_IPSET_FIXED = os.getenv('GLOBAL_IPSET_FIXED')
REGIONAL_IPSET_DYNAMIC = os.getenv('REGIONAL_IPSET_DYNAMIC')
REGIONAL_IPSET_FIXED = os.getenv('REGIONAL_IPSET_FIXED')

def dynamic_ip_handler(publicIp, user_name, user_email):
    publicIp = [publicIp+'/32']
    message = update_ipset(GLOBAL_IPSET_DYNAMIC, REGIONAL_IPSET_DYNAMIC, publicIp, user_name, action = 'INSERT')
    print(data_log(publicIp, user_name, user_email, type = 'waf_dynamic'))
    return message

def fixed_ip_handler(publicIp, user_name, user_email):
    if user_authorization(user_name, user_email, type = 'admin'):
        publicIp = [publicIp+'/32']
        message = update_ipset(GLOBAL_IPSET_FIXED, REGIONAL_IPSET_FIXED, publicIp, user_name, action = 'INSERT')
        print(data_log(publicIp, user_name, user_email, type = 'waf_fixed'))
        return message
    else:
        return f'{user_name}, you are not authorized to execute this command, please contact your administrators'

def clean_ips_handler(user_name, user_email):
    if user_authorization(user_name, user_email, type = 'admin'):
        global_ips, regional_ips = clean_ipset(GLOBAL_IPSET_DYNAMIC, REGIONAL_IPSET_DYNAMIC, user_name)
        print(data_log(global_ips, user_name, user_email, type = 'clean-global'))
        print(data_log(regional_ips, user_name, user_email, type = 'clean-regional'))
        return f"Dynamic ips have been cleaned"