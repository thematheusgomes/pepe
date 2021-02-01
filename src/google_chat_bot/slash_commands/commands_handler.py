import src.aws_waf.waf as waf
from ipaddress import ip_address
from src.aws_sg.security_group import security_group_handler
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
    if args[0] == 'dynamic' and validate_ip(args[1]):
        return waf.dynamic_ip_handler(args[1], user_name, user_email)
    elif args[0] == 'fixed' and validate_ip(args[1]):
        return waf.fixed_ip_handler(args[1], user_name, user_email)
    elif args[0] == 'clean':
        return waf.clean_ips_handler(user_name, user_email)
    elif args[0] == 'help':
        return f'Hey {user_name},\n\nI\'ll show you the arguments you can use with the `iprelease` command:\n\n-> /iprelease `<publicIp>`\n-> /iprelease dynamic `<publicIp>`\n-> /iprelease fixed `<publicIp>`\n-> /iprelease clean\n\nTo find out what is your public ip access the link http://checkip.amazonaws.com'
    elif validate_ip(args[0]):
        return waf.dynamic_ip_handler(args[0], user_name, user_email)
    else:
        LOGGER.error(f'Invalid arguments: {args}')
        return 'Invalid arguments\n\nThis command will accept only the following arguments:\n\n-> /iprelease `<publicIp>`\n-> /iprelease dynamic `<publicIp>`\n-> /iprelease fixed `<publicIp>`\n-> /iprelease clean\n-> /iprelease help\n\nTo find out what is your public ip access the link http://checkip.amazonaws.com'

def sg_ip_release_handler(args, user_name, user_email):
    if args[0] == 'dev' or args[0] == 'qa' or args[0] == 'prod' or args[0] == 'tools' and validate_ip(args[1]):
        return security_group_handler(args[0], args[1], user_name, user_email)
    else:
        LOGGER.error(f'Invalid arguments: {args}')
        return 'Invalid arguments\n\nThis command will accept only the following arguments:\n\n> /sgiprelease dev `<publicIp>`\n> /sgiprelease qa `<publicIp>`\n> /sgiprelease prod `<publicIp>`\n> /sgiprelease tools `<publicIp>`'

def validate_ip(publicIp):
    try:
        if ip_address(publicIp).is_private:
            LOGGER.error(f'Invalid IP address: {publicIp}, ip address must be public and not private')
            return False
        else:
            LOGGER.info(f'Valid IP address: {publicIp}')
            return True
    except Exception as e:
        LOGGER.error(e)
        return False
