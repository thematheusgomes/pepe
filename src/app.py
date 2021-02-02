import json
from src.log import Logger
from src.alerts.alerts import hund_alerts_handler, awslogs_handler
from src.bot.slash_commands.commands_handler import select_command
from src.bot.bot_authorization import authorization

LOGGER = Logger()

def handler(event, context):
    """Handles an event from Google Chat."""
    LOGGER.info(f'Event: {json.dumps(event)}')
    message = filter_events(event)
    return response(message)

def filter_events(event):
    if 'awslogs' in event.keys():
        LOGGER.info('Request type: AWS Logs')
        awslogs_handler(event)
    elif event['path'] == '/googlechat':
        LOGGER.info('Request type: Pepe Bot')
        return bot_handler(event)
    elif event['path'] == '/hundio':
        LOGGER.info('Request type: Hund Alerts')
        hund_alerts_handler(event)
    else:
        LOGGER.error('Invalid event')

def bot_handler(event):
    token = event['headers']['Authorization'].replace('Bearer ', '')
    event = json.loads(event['body'])
    # Check the authenticity of the token sent
    authorization(token)
    user_email = event['user']['email']
    user_name = event['user']['displayName'] if event['user']['displayName'] else 'Dear'
    if event['type'] == 'ADDED_TO_SPACE' and 'singleUserBotDm' in event['space'].keys():
        message = f'Thanks for starting to chat with me {user_name}, I will be very happy to help you!\n\nThe commands I have available are:\n\n-> `/iprelease`\n-> `/sgipupdate`'
        LOGGER.info(f'User {user_name} starts a conversation with Pepe')
    elif event['type'] == 'ADDED_TO_SPACE' and 'singleUserBotDm' not in event['space'].keys():
        message = 'Thanks for adding me to "%s"!' % (event['space']['displayName'] if event['space']['displayName'] else 'this chat')
        LOGGER.info('Pepe was added to room "%s"' % (event['space']['displayName'] if event['space']['displayName'] else 'unknown'))
    elif event['type'] == 'MESSAGE' and 'slashCommand' not in event['message'].keys():
        message = f'Sorry {user_name}, I\'m currently accepting only slash commands!\n\n*Commands List:*\n\n-> `/iprelease`\n-> `/sgipupdate`\n\nIf the problem persists, try typing slash "/" then select the command you want from the command list that will appear.'
    elif event['type'] == 'MESSAGE' and 'slashCommand' in event['message'].keys():
        message = select_command(event, user_name, user_email)
    else:
        message = 'Invalid event type'
        LOGGER.error(message)
    return message

def response(message):
    LOGGER.info('Sending the message to Google Chat')
    return ({
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "text": message
            })
        })
