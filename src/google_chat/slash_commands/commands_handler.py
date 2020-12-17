from log import Logger
from google_chat.slash_commands.ip_release import ip_release_handler

LOGGER = Logger()

def slash_command_handler(event, user_name, user_email):
    text = validate_commands(event, user_name, user_email)
    return text

def validate_commands(event, user_name, user_email):
    commandId = event['message']['slashCommand']['commandId']
    commandName = event['message']['annotations'][0]['slashCommand']['commandName']
    args = event['message']['argumentText'].split(' ')
    if args[0] == '':
        del args[0]
    if commandId == '1':
        LOGGER.info(f'Command performed: {commandName}')
        text = ip_release_handler(args, user_name, user_email)
        return text
