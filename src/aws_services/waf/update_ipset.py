import boto3
from src.log import Logger

LOGGER = Logger()

def update_ipset(global_ipset, regional_ipset, ip_list, user_name, action):
    params = constructor(ip_list, action)
    update_ip_on_global_ipset(global_ipset, user_name, params, action)
    message = update_ip_on_regional_ipset(regional_ipset, user_name, params, action)
    return message

def update_ip_on_global_ipset(global_ipset, user_name, params, action):
    LOGGER.info(f'Action {action} will be performed on global ipset {global_ipset}')
    try:
        waf_global = boto3.client('waf')
        global_token = waf_global.get_change_token()
        waf_global.update_ip_set(
            IPSetId=global_ipset,
            ChangeToken=global_token['ChangeToken'],
            Updates=params
        )
        LOGGER.info(f'Action {action} was successfully performed')
    except Exception as e:
        LOGGER.error(e)
        return f'Something went wrong when releasing your IP in the global list {user_name}, please contact your administrator'

def update_ip_on_regional_ipset(regional_ipset, user_name, params, action):
    LOGGER.info(f'Action {action} will be performed on regional ipset {regional_ipset}')
    try:
        waf_regional = boto3.client('waf-regional')
        regional_token = waf_regional.get_change_token()
        waf_regional.update_ip_set(
            IPSetId=regional_ipset,
            ChangeToken=regional_token['ChangeToken'],
            Updates=params
        )
        LOGGER.info(f'Action {action} was successfully performed')
        return f'{user_name}, your ip has been released and now you can access Agent Portal and Superset'
    except Exception as e:
        LOGGER.error(e)
        return f'Something went wrong when releasing your IP in the regional list {user_name}, please contact your administrator'

def constructor(ip_list, action):
    params = []
    for ip in ip_list:
        params.append(
            {
                'Action': action,
                'IPSetDescriptor': {
                    'Type': ip['Version'],
                    'Value': ip['IpAddress']
                }
            }
        )
    return params
