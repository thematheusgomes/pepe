import json
import boto3
from log import Logger

LOGGER = Logger()

def allow_ip_on_global_ipset(global_ipset, publicIp, user_name):
    try:
        LOGGER.info(f'{user_name} public ip will be added to IPSET Global')
        waf_global = boto3.client('waf')
        global_token = waf_global.get_change_token()
        waf_global.update_ip_set(
            IPSetId=global_ipset,
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
        LOGGER.info(f'IP added in ipset {global_ipset}')
        return f'{user_name}, your ip ({publicIp}) has been released and now you can access Agent Portal and Superset'
    except Exception as e:
        LOGGER.error(e)
        return f'Something went wrong when releasing your IP {user_name}, please contact your administrator'

def allow_ip_on_regional_ipset(regional_ipset, publicIp, user_name):
    LOGGER.info(f'{user_name} public ip will be added to IPSET Regional')
    try:
        waf_regional = boto3.client('waf-regional')
        regional_token = waf_regional.get_change_token()
        waf_regional.update_ip_set(
            IPSetId=regional_ipset,
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
        LOGGER.info(f'IP added in ipset {regional_ipset}')
        return f'{user_name}, your ip ({publicIp}) has been released and now you can access Agent Portal and Superset'
    except Exception as e:
        LOGGER.error(e)
        return f'Something went wrong when releasing your IP {user_name}, please contact your administrator'
