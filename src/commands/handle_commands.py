import src.aws.waf.handle_ipset as ipset
import src.aws.lambda_function.handle_lambda as _lambda
from ipaddress import ip_address, IPv4Address
from src.aws.ec2.handle_security_groups import security_group_handler
from src.logger import Logger

logger = Logger()

def select_command(event, user_name, user_email):
    if 'argumentText' not in event['message']:
        return f'You have not passed any arguments, please try to run one of the options below:\n\n-> `/iprelease <publicIp>` (Add your ip to the dynamic ips list)\n-> `/iprelease dynamic <publicIp>` (Another option that add your ip to the dynamic ips list)\n-> `/iprelease fixed <publicIp>` (Add your ip to the fixed ips list)\n-> `/iprelease clean` (Remove all ips from dynamic ips list)\n-> `/sgipupdate help` (Shows a message similar to that with all accepted arguments for this command)\n-> `/turnonoff help` (Shows a message similar to that with all accepted arguments for this command)\n\nTo find out what is your public ip access the link http://checkip.amazonaws.com'
    arguments = event['message']['argumentText'].split(' ')
    commandId = event['message']['slashCommand']['commandId']
    commandName = event['message']['annotations'][0]['slashCommand']['commandName']
    logger.info(f'Command performed: {commandName}')

    if arguments[0] == '':
        del arguments[0]

    logger.info(f'Arguments: {arguments}')
    if commandId == '1':
        return iprelease_command(arguments, user_name, user_email)
    elif commandId == '2':
        return sgipupdate_command(arguments, user_name, user_email)
    elif commandId == '3':
        return turnonoff_command(arguments, user_name, user_email)

def iprelease_command(arguments, user_name, user_email):
    help_message = f'Hey {user_name},\n\nYou passed wrong arguments, this command allows the following arguments:\n\n-> `/iprelease <publicIp>` (Add your ip to the dynamic ips list)\n-> `/iprelease dynamic <publicIp>` (Another option that add your ip to the dynamic ips list)\n-> `/iprelease fixed <publicIp>` (Add your ip to the fixed ips list)\n-> `/iprelease clean` (Remove all ips from dynamic ips list)\n\nTo find out what is your public ip access the link http://checkip.amazonaws.com'
    try:
        if len(arguments) == 2 and ip_address(arguments[1]).is_global:
            if 'dynamic' in arguments[0]:
                return ipset.dynamic_ip_handler(ip_version(arguments[1]), user_name, user_email)
            elif 'fixed' in arguments[0]:
                return ipset.fixed_ip_handler(ip_version(arguments[1]), user_name, user_email)
        if len(arguments) == 1:
            if 'clean' in arguments[0]:
                return ipset.clean_ips_handler(user_name, user_email)
            elif 'help' in arguments[0]:
                return help_message
            elif ip_address(arguments[0]).is_global:
                return ipset.dynamic_ip_handler(ip_version(arguments[0]), user_name, user_email)
        else:
            return help_message
    except Exception as e:
        logger.exception(e)
        return help_message

def sgipupdate_command(arguments, user_name, user_email):
    help_message = f'Hey {user_name},\n\nYou passed wrong arguments, this command allows the following arguments:\n\n-> `/sgipupdate dev <publicIp>` (Update IP in the Dev Security Group)\n-> `/sgipupdate qa <publicIp>` (Update IP in the Qa Security Group)\n-> `/sgipupdate prod <publicIp>` (Update IP in the Prod Security Group)\n-> `/sgipupdate tools <publicIp>` (Update IP in the Tools Security Group)\n\nTo find out what is your public ip access the link http://checkip.amazonaws.com'
    try:
        if len(arguments) == 2 and ip_address(arguments[1]).is_global:
            return security_group_handler(arguments[0], arguments[1], user_name, user_email)
        elif arguments[0] == 'help':
            return help_message
        else:
            logger.error(f'Invalid arguments')
            return help_message
    except Exception as e:
        logger.exception(e)
        return help_message

def turnonoff_command(arguments, user_name, user_email):
    help_message = f'Hey {user_name},\n\nYou passed wrong arguments, this command allows the following arguments:\n\n-> `/turnonoff` <action> <environment> <target>\n\n*supported actions:* [start, stop];\n*supported environments:* [dev, qa, tools] (tools is only supported for target bastion)\n*supported targets:* [bastion, clusters] (Clusters include ECS + RDS)'
    if len(arguments) > 5 or len(arguments) < 3 or 'help' in arguments:
        logger.error('Invalid arguments...')
        return help_message
    return _lambda.handle_turn_on_off_function(arguments, user_name, user_email)

def ip_version(ip):
    ipv = []
    try:
        if type(ip_address(ip)) is IPv4Address:
            ipv.append({'IpAddress': ip + '/32', 'Version': 'IPV4'})
        else:
            ipv.append({'IpAddress': ip + '/128', 'Version': 'IPV6'})
        logger.info(f'IP(s): {ipv}')
        return ipv
    except Exception as e:
        logger.error(e)
