import boto3
from log import Logger
import aws_waf.update_ipset as waf

LOGGER = Logger()

def clean_ipset(global_ipset, regional_ipset, user_name):
    global_ips = get_global_ipset(global_ipset, publicIps = [])
    regional_ips = get_regional_ipset(regional_ipset, publicIps = [])
    global_params = waf.constructor(global_ips, action = 'DELETE')
    regional_params = waf.constructor(regional_ips, action = 'DELETE')
    waf.update_ip_on_global_ipset(global_ipset, user_name, global_params, action = 'DELETE')
    waf.update_ip_on_regional_ipset(regional_ipset, user_name, regional_params, action = 'DELETE')
    return global_ips, regional_ips

def get_global_ipset(global_ipset, publicIps):
    try:
        global_client = boto3.client('waf')
        response = global_client.get_ip_set(IPSetId=global_ipset)
        for ip in response['IPSet']['IPSetDescriptors']:
            publicIps.append(ip['Value'])
        LOGGER.info('Global ips list was successfully generated')
        return publicIps
    except Exception as e:
        LOGGER.error(e)

def get_regional_ipset(global_ipset, publicIps):
    try:
        regional_client = boto3.client('waf-regional')
        response = regional_client.get_ip_set(IPSetId=global_ipset)
        for ip in response['IPSet']['IPSetDescriptors']:
            publicIps.append(ip['Value'])
        LOGGER.info('Regional ips list was successfully generated')
        return publicIps
    except Exception as e:
        LOGGER.error(e)
