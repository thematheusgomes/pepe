import os
import boto3
from ipaddress import ip_address, IPv4Address
from src.security.user_authorization import user_authorization
from src.logger import Logger

logger = Logger()

DEV_SGID = os.getenv('DEV_SGID')
QA_SGID = os.getenv('QA_SGID')
PROD_SGID = os.getenv('PROD_SGID')
TOOLS_SGID = os.getenv('TOOLS_SGID')

def security_group_handler(environment, public_ip, user_name, user_email):
    ec2 = boto3.resource('ec2')
    if environment == 'dev' and (user_authorization(user_name, user_email, type = 'dev') or user_authorization(user_name, user_email, type = 'admin')):
        security_group = ec2.SecurityGroup(DEV_SGID)
        ip_recorded = get_public_ips_from_sg(security_group)
    elif environment == 'qa' and (user_authorization(user_name, user_email, type = 'dev') or user_authorization(user_name, user_email, type = 'admin')):
        security_group = ec2.SecurityGroup(QA_SGID)
        ip_recorded = get_public_ips_from_sg(security_group)
    elif environment == 'prod' and user_authorization(user_name, user_email, type = 'admin'):
        security_group = ec2.SecurityGroup(PROD_SGID)
        ip_recorded = get_public_ips_from_sg(security_group)
    elif environment == 'tools' and user_authorization(user_name, user_email, type = 'admin'):
        security_group = ec2.SecurityGroup(TOOLS_SGID)
        ip_recorded = get_public_ips_from_sg(security_group)
    else:
        if environment not in ['dev', 'qa', 'prod', 'tools']:
            return f'{user_name} this `{environment}` environment is not valid, please enter one of these environments `dev`, `qa`, `prod` and `tools`'
        return f'{user_name} you are not authorized to perform this command, please contact your administrator'

    revoke_ingress(environment, security_group, user_name, ip_recorded)
    message = authorize_ingress(environment, security_group, user_name, public_ip)
    return message

def get_public_ips_from_sg(security_group):
    ip_recorded = {}
    for ip_list in security_group.ip_permissions:
        if 'FromPort' in ip_list.keys() and ip_list['FromPort'] == 22:
            ip_recorded['IPv4Ranges'] = ip_list['IpRanges']
            ip_recorded['IPv6Ranges'] = ip_list['Ipv6Ranges']
    return ip_recorded

def revoke_ingress(environment, security_group, user_name, ip_recorded):
    revoke_list = revoke_ingress_constructor(ip_recorded, user_name)
    try:
        response = security_group.revoke_ingress(
            IpPermissions=[revoke_list]
        )
        logger.info(f'Response {environment} revocation: {response}')
    except Exception as e:
        logger.error(e)

def authorize_ingress(environment, security_group, user_name, public_ip):
    authorize_list = authorize_ingress_constructor(public_ip, user_name)
    try:
        response = security_group.authorize_ingress(
            IpPermissions=[authorize_list]
        )
        logger.info(f'Response {environment} authorization: {response}')
        return f'{user_name} your public ip was authorized on {environment} security group, now you should be able to access the {environment} clusters, if you have any problems contact the administrators'
    except Exception as e:
        logger.error(e)
        return f'Something went wrong when releasing your IP {user_name}, please contact your administrator'

def revoke_ingress_constructor(ip_recorded, user_name):
    revoke_list = {
        'FromPort': 22,
        'IpProtocol': 'tcp',
        'IpRanges': [],
        'Ipv6Ranges': [],
        'ToPort': 22
    }
    for ip in ip_recorded['IPv4Ranges']:
        if ip['Description'] == user_name:
            revoke_list['IpRanges'].append(ip)
    for ip in ip_recorded['IPv6Ranges']:
        if ip['Description'] == user_name:
            revoke_list['Ipv6Ranges'].append(ip)
    if len(revoke_list['IpRanges']) == 0 and len(revoke_list['Ipv6Ranges']) == 0:
        logger.info('No previously registered ip was found')
    return revoke_list

def authorize_ingress_constructor(public_ip, user_name):
    authorize_list = {
        'FromPort': 22,
        'IpProtocol': 'tcp',
        'IpRanges': [],
        'Ipv6Ranges': [],
        'ToPort': 22
    }
    try:
        if type(ip_address(public_ip)) is IPv4Address:
            authorize_list['IpRanges'].append({'CidrIp': public_ip + '/32', 'Description': user_name})
        else:
            authorize_list['Ipv6Ranges'].append({'CidrIpv6': public_ip + '/128', 'Description': user_name})
        return authorize_list
    except Exception as e:
        logger.error(e)
