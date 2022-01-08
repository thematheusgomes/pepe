import boto3
from src.logger import Logger
import src.aws.waf.update_ipset as waf

logger = Logger()

def clean_ipset(global_ipset, regional_ipset, user_name):
    global_ips = get_global_ipset(global_ipset, publicIps = [])
    regional_ips = get_regional_ipset(regional_ipset, publicIps = [])
    global_params = waf.constructor(global_ips, action = 'DELETE')
    regional_params = waf.constructor(regional_ips, action = 'DELETE')
    waf.update_ip_on_global_ipset(global_ipset, user_name, global_params, action = 'DELETE')
    waf.update_ip_on_regional_ipset(regional_ipset, user_name, regional_params, action = 'DELETE')
    logger.info(f'IPs removed from the Global list: {global_ips}')
    logger.info(f'IPs removed from the Regional list: {regional_ips}')

def get_global_ipset(global_ipset, publicIps):
    try:
        global_client = boto3.client('waf')
        response = global_client.get_ip_set(IPSetId=global_ipset)
        for ip in response['IPSet']['IPSetDescriptors']:
            publicIps.append(ip_version(ip['Value']))
        logger.info('Global ips list was successfully generated')
        return publicIps
    except Exception as e:
        logger.error(e)

def get_regional_ipset(global_ipset, publicIps):
    try:
        regional_client = boto3.client('waf-regional')
        response = regional_client.get_ip_set(IPSetId=global_ipset)
        for ip in response['IPSet']['IPSetDescriptors']:
            publicIps.append(ip_version(ip['Value']))
        logger.info('Regional ips list was successfully generated')
        return publicIps
    except Exception as e:
        logger.error(e)

def ip_version(ip):
    try:
        if '/32' in ip:
            return {'IpAddress': ip, 'Version': 'IPV4'}
        elif '/128' in ip:
            return {'IpAddress': ip, 'Version': 'IPV6'}
    except Exception as e:
        logger.error(e)
