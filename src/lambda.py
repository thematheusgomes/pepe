import os
from main.ip_release import ip_release_handler
from main.log import Logger
from main.util import send_slack_message, response_builder


LOGGER = Logger()

def help_handler (arguments):
    """
    *Action:* help
    *Description:* This action allows list available commands or command specific instructions

    *Arguments:*
    action : help
    command: (optional)
    

    """
    num_of_arguments = 2
    # general help
    if len(arguments) < num_of_arguments:
        result = ['List of available commands, for more use `help <command>`:']
        for key, value in switcher.items():
            result.append(key)
        return '\n'.join(result)
    # command specific help
    elif len(arguments) == num_of_arguments:
        command = switcher.get(arguments[1], lambda: "Invalid command")
        return command.__doc__
    else:
        return 'Sorry, I did not get that, please type help or help <command>.'

    
    #return {'action': 'help', 'message': 'TODO implement help for commands'}

def ip_release(arguments):
    """
    *Action:* waf
    *Description:* This action allows an new IP address on WAF given the location.
    It is possible for location to have Global and Regional WAF, in such
    case, waf action will allow IP address in both WAFs.
    *Arguments:*

    action : waf
    location : mx || br || us || song || mariano || john || andres
    ip: IP Address on CIDR notation

    *Example:*
    `waf br 0.0.0.0/32`
    """
    # num_of_arguments should account 'action', since arguments[0] is the action itself
    num_of_arguments = 3
    if len(arguments) > num_of_arguments:
        return 'This action takes exactly 2 arguments: <location> <CIDR>'
    else:
        ip_release_event = {
            "action": arguments[0],
            "location": arguments[1],
            "ip": arguments[2] 
        }
        result = ip_release_handler(ip_release_event)
        return result['message']

switcher = {
    'waf': ip_release,
    'help': help_handler
}

def handler(data, context):
    """Handle an incoming HTTP request from a Slack chat-bot.
    """
    # Slack Verification
    if 'challenge' in data:
        return data['challenge']
    else:
        slack_event = data['event']
        text = slack_event['text'].split()
        action = text[0]

        channel_id = slack_event["channel"]
        # get action 
        command = switcher.get(action, lambda: "Invalid command")
        # execut action
        message = command(text)
        
        if send_slack_message(channel_id,message):
            LOGGER.info('Pepe replied slack message')
        else:
            LOGGER.info('Pepe did not replied slack message')
