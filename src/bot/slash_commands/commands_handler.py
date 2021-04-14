import src.aws_services.waf.waf as waf
from ipaddress import ip_address, IPv4Address
from src.aws_services.ec2.security_group import security_group_handler
from src.log import Logger

LOGGER = Logger()

def select_command(event, user_name, user_email):
    args = event['message']['argumentText'].split(' ')
    commandId = event['message']['slashCommand']['commandId']
    commandName = event['message']['annotations'][0]['slashCommand']['commandName']
    LOGGER.info(f'Command performed: {commandName}')
    if args[0] == '':
        del args[0]
    if commandId == '1':
        message = waf_ip_release_handler(args, user_name, user_email)
        return message
    if commandId == '2':
        message = sg_ip_release_handler(args, user_name, user_email)
        return message

def waf_ip_release_handler(args, user_name, user_email):
    if len(args) in range(3):
        if args[0] == 'dynamic' and ip_address(args[1]).is_global:
            return waf.dynamic_ip_handler(args[1], user_name, user_email)
        elif args[0] == 'fixed' and ip_address(args[1]).is_global:
            return waf.fixed_ip_handler(args[1], user_name, user_email)
        elif args[0] == 'clean':
            return waf.clean_ips_handler(user_name, user_email)
        elif args[0] == 'help':
            return f'Hey {user_name},\n\nI\'ll show you the arguments you can use with the `iprelease` command:\n\n-> `/iprelease <publicIp>` (Add your ip to the dynamic ips list)\n-> `/iprelease dynamic <publicIp>` (Another option that add your ip to the dynamic ips list)\n-> `/iprelease fixed <publicIp>` (Add your ip to the fixed ips list)\n-> `/iprelease clean` (Remove all ips from dynamic ips list)\n\nTo find out what is your public ip access the link http://checkip.amazonaws.com'
        elif ip_address(args[0]).is_global:
            ipv = ip_version(args[0])
            return waf.dynamic_ip_handler(ipv, user_name, user_email)
        else:
            LOGGER.error(f'Invalid arguments: {args}')
            return f'Hey {user_name},\n\nThis argument is invalid, currently I\'m accepting only the arguments below:\n\n-> `/sgipupdate help` (Shows a message similar to that with all accepted arguments for this command)\n-> `/iprelease <publicIp>` (Add your ip to the dynamic ips list)\n-> `/iprelease dynamic <publicIp>` (Another option that add your ip to the dynamic ips list)\n-> `/iprelease fixed <publicIp>` (Add your ip to the fixed ips list)\n-> `/iprelease clean` (Remove all ips from dynamic ips list)\n\nTo find out what is your public ip access the link http://checkip.amazonaws.com'
    else:
        LOGGER.error(f'Exceeded the argument limit: {len(args)}')
        return f'Hey {user_name},\n\nYou have exceeded the argument limit, for this command you can only put up to a maximum of 2 arguments.\n\nIf you want to understand a little better how it works, just type `/iprelease help`'

def sg_ip_release_handler(args, user_name, user_email):
    if args[0] == 'dev' or args[0] == 'qa' or args[0] == 'prod' or args[0] == 'tools' and ip_address(args[1]).is_global:
        return security_group_handler(args[0], args[1], user_name, user_email)
    elif args[0] == 'help':
        return f'Hey {user_name},\n\nI\'ll show you the arguments you can use with the `sgipupdate` command:\n\n-> `/sgipupdate dev <publicIp>` (Update IP in the Dev Security Group)\n-> `/sgipupdate qa <publicIp>` (Update IP in the Qa Security Group)\n-> `/sgipupdate prod <publicIp>` (Update IP in the Prod Security Group)\n-> `/sgipupdate tools <publicIp>` (Update IP in the Tools Security Group)\n\nTo find out what is your public ip access the link http://checkip.amazonaws.com'
    else:
        LOGGER.error(f'Invalid arguments: {args}')
        return f'Hey {user_name},\n\nThis argument is invalid, currently I\'m accepting only the arguments below:\n\n-> `/sgipupdate help` (Shows a message similar to that with all accepted arguments for this command)\n-> `/sgipupdate dev <publicIp>` (Update IP in the Dev Security Group)\n-> `/sgipupdate qa <publicIp>` (Update IP in the Qa Security Group)\n-> `/sgipupdate prod <publicIp>` (Update IP in the Prod Security Group)\n-> `/sgipupdate tools <publicIp>` (Update IP in the Tools Security Group)\n\nTo find out what is your public ip access the link http://checkip.amazonaws.com'

def ip_version(ip):
    ipv = []
    try:
        if type(ip_address(ip)) is IPv4Address:
            ipv.append({'IpAddress': ip + '/32', 'Version': 'IPV4'})
        else:
            ipv.append({'IpAddress': ip + '/128', 'Version': 'IPV6'})
        LOGGER.info(f'IP Version: {ipv}')
        return ipv
    except Exception as e:
        LOGGER.error(e)
