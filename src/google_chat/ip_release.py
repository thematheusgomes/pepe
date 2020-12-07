import os
import boto3
from log import Logger

LOGGER = Logger()
REGINAL_IPSET = os.getenv('REGINAL_IPSET')
GLOBAL_IPSET = os.getenv('GLOBAL_IPSET')

def ip_release_handler(publicIp, user_name):
    allow_ip_on_global_ipset(publicIp, user_name)
    allow_ip_on_regional_ipset(publicIp, user_name)
    return f'{user_name}, your ip ({publicIp}) has been released and now you can access Agent Portal and Superset'


def allow_ip_on_global_ipset(publicIp, user_name):
    try:
        LOGGER.info(f'{user_name} will perform changes on Global WAF')
        waf_global = boto3.client('waf')
        global_token = waf_global.get_change_token()
        waf_global.update_ip_set(
            IPSetId=GLOBAL_IPSET,
            ChangeToken=global_token['ChangeToken'],
            Updates=[
                {
                    'Action': 'INSERT',
                    'IPSetDescriptor': {
                        'Type': 'IPV4',
                        'Value': publicIp+'/32'
                    }
                }
            ]
        )
    except Exception as e:
        LOGGER.error(e)
        return f'Something went wrong when releasing your IP {user_name}, please contact your administrator'

def allow_ip_on_regional_ipset(publicIp, user_name):
    LOGGER.info(f'{user_name} will perform changes on Regional WAF')
    try:
        waf_regional = boto3.client('waf-regional')
        regional_token = waf_regional.get_change_token()
        waf_regional.update_ip_set(
            IPSetId=REGINAL_IPSET,
            ChangeToken=regional_token['ChangeToken'],
            Updates=[
                {
                    'Action': 'INSERT',
                    'IPSetDescriptor': {
                        'Type': 'IPV4',
                        'Value': publicIp+'/32'
                    }
                }
            ]
        )
    except Exception as e:
        LOGGER.error(e)
        return f'Something went wrong when releasing your IP {user_name}, please contact your administrator'
