import os
import boto3
from src.google_chat_bot.user_authorization import user_authorization
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
            revoke_previous_ip(arg, security_group, user_name, ipreg = security_group.ip_permissions[0])
            text = authorize_ingress(arg, security_group, user_name, publicIp)
            print(data_log(publicIp, user_name, user_email, type = 'sg_dev'))
            return text
        else:
            return f'{user_name} you are not authorized to peform this command, please contact your administrator'
    elif arg == 'qa':
        if user_authorization(user_name, user_email, type = 'dev') or user_authorization(user_name, user_email, type = 'admin'):
            security_group = ec2.SecurityGroup(QA_SGID)
            revoke_previous_ip(arg, security_group, user_name, ipreg = security_group.ip_permissions[0])
            text = authorize_ingress(arg, security_group, user_name, publicIp)
            print(data_log(publicIp, user_name, user_email, type = 'sg_qa'))
            return text
        else:
            return f'{user_name} you are not authorized to peform this command, please contact your administrator'
    elif arg == 'prod':
        if user_authorization(user_name, user_email, type = 'admin'):
            security_group = ec2.SecurityGroup(PROD_SGID)
            revoke_previous_ip(arg, security_group, user_name, ipreg = security_group.ip_permissions[2])
            text = authorize_ingress(arg, security_group, user_name, publicIp)
            print(data_log(publicIp, user_name, user_email, type = 'sg_prod'))
            return text
        else:
            return f'{user_name} you are not authorized to peform this command, please contact your administrator'
    elif arg == 'tools':
        if user_authorization(user_name, user_email, type = 'admin'):
            security_group = ec2.SecurityGroup(TOOLS_SGID)
            revoke_previous_ip(arg, security_group, user_name, ipreg = security_group.ip_permissions[0])
            text = authorize_ingress(arg, security_group, user_name, publicIp)
            print(data_log(publicIp, user_name, user_email, type = 'sg_tools'))
            return text
        else:
            return f'{user_name} you are not authorized to peform this command, please contact your administrator'

def revoke_previous_ip(arg, security_group, user_name, ipreg):
    count = 0
    for ip in ipreg['IpRanges']:  
        if ip['Description'] == user_name:
            count += 1
            revoke_ingress(arg, security_group, user_name, ip['CidrIp'])
    if count == 0:
        LOGGER.error('No previously registered ip was found')

def revoke_ingress(arg, security_group, user_name, publicIp):
    try:
        security_group.revoke_ingress(
            IpPermissions=[
                {
                    'FromPort': 22,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': publicIp,
                            'Description': user_name
                        },
                    ],
                    'ToPort': 22
                },
            ]
        )
        LOGGER.info(f'The IP {publicIp} has been revoked in security group boomcredit-{arg}-bastion')
    except Exception as e:
        LOGGER.error(e)

def authorize_ingress(arg, security_group, user_name, publicIp):
    try:
        security_group.authorize_ingress(
            IpPermissions=[
                {
                    'FromPort': 22,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': publicIp+'/32',
                            'Description': user_name
                        },
                    ],
                    'ToPort': 22
                },
            ]
        )
        LOGGER.info(f'The IP {publicIp}/32 has been authorized in security group boomcredit-{arg}-bastion')
        return f'{user_name} your public ip was authorized on {arg} security group, now you should be able to access the {arg} clusters, if you have any problems contact the administrators'
    except Exception as e:
        LOGGER.error(e)
        return f'Something went wrong when releasing your IP {user_name}, please contact your administrator'
