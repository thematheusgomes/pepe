import os
import boto3
from ipaddress import ip_address, IPv4Address
from src.bot.user_authorization import user_authorization
from src.log import Logger, data_log

LOGGER = Logger()

DEV_SGID = os.getenv('DEV_SGID')
QA_SGID = os.getenv('QA_SGID')
PROD_SGID = os.getenv('PROD_SGID')
TOOLS_SGID = os.getenv('TOOLS_SGID')

def security_group_handler(arg, publicIp, user_name, user_email):
    ec2 = boto3.resource('ec2')
    if arg == 'dev':
        if user_authorization(user_name, user_email, type = 'dev') or user_authorization(user_name, user_email, type = 'admin'):
            security_group = ec2.SecurityGroup(DEV_SGID)
            revoke_ingress(arg, security_group, user_name, ip_recorded = security_group.ip_permissions[0])
            message = authorize_ingress(arg, security_group, user_name, publicIp)
            print(data_log(publicIp, user_name, user_email, type = 'sg_dev'))
            return message
        else:
            return f'{user_name} you are not authorized to peform this command, please contact your administrator'
    elif arg == 'qa':
        if user_authorization(user_name, user_email, type = 'dev') or user_authorization(user_name, user_email, type = 'admin'):
            security_group = ec2.SecurityGroup(QA_SGID)
            revoke_ingress(arg, security_group, user_name, ip_recorded = security_group.ip_permissions[0])
            message = authorize_ingress(arg, security_group, user_name, publicIp)
            print(data_log(publicIp, user_name, user_email, type = 'sg_qa'))
            return message
        else:
            return f'{user_name} you are not authorized to peform this command, please contact your administrator'
    elif arg == 'prod':
        if user_authorization(user_name, user_email, type = 'admin'):
            security_group = ec2.SecurityGroup(PROD_SGID)
            revoke_ingress(arg, security_group, user_name, ip_recorded = security_group.ip_permissions[2])
            message = authorize_ingress(arg, security_group, user_name, publicIp)
            print(data_log(publicIp, user_name, user_email, type = 'sg_prod'))
            return message
        else:
            return f'{user_name} you are not authorized to peform this command, please contact your administrator'
    elif arg == 'tools':
        if user_authorization(user_name, user_email, type = 'admin'):
            security_group = ec2.SecurityGroup(TOOLS_SGID)
            revoke_ingress(arg, security_group, user_name, ip_recorded = security_group.ip_permissions[0])
            message = authorize_ingress(arg, security_group, user_name, publicIp)
            print(data_log(publicIp, user_name, user_email, type = 'sg_tools'))
            return message
        else:
            return f'{user_name} you are not authorized to peform this command, please contact your administrator'

def revoke_ingress(arg, security_group, user_name, ip_recorded):
    revoke_list = revoke_ingress_constructor(ip_recorded, user_name)
    try:
        response = security_group.revoke_ingress(
            IpPermissions=[revoke_list]
        )
        LOGGER.info(f'Response {arg} revocation: {response}')
    except Exception as e:
        LOGGER.error(e)

def authorize_ingress(arg, security_group, user_name, publicIp):
    authorize_list = authorize_ingress_constructor(publicIp, user_name)
    try:
        response = security_group.authorize_ingress(
            IpPermissions=[authorize_list]
        )
        LOGGER.info(f'Response {arg} authorization: {response}')
        return f'{user_name} your public ip was authorized on {arg} security group, now you should be able to access the {arg} clusters, if you have any problems contact the administrators'
    except Exception as e:
        LOGGER.error(e)
        return f'Something went wrong when releasing your IP {user_name}, please contact your administrator'

def revoke_ingress_constructor(ipreg, user_name):
    revoke_list = {
        'FromPort': 22,
        'IpProtocol': 'tcp',
        'IpRanges': [],
        'Ipv6Ranges': [],
        'ToPort': 22
    }
    for ip in ipreg['IpRanges']:
        if ip['Description'] == user_name:
            revoke_list['IpRanges'].append(ip)
    if 'Ipv6Ranges' in ipreg:
        for ip in ipreg['Ipv6Ranges']:
            if ip['Description'] == user_name:
                revoke_list['Ipv6Ranges'].append(ip)
    if len(revoke_list['IpRanges']) == 0 and len(revoke_list['Ipv6Ranges']) == 0:
        LOGGER.error('No previously registered ip was found')
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
        LOGGER.error(e)
