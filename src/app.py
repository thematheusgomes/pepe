import json
from src.log import Logger
from src.google_chat_alerts.alerts import hund_alerts_handler, awslogs_handler
from src.google_chat.slash_commands.commands_handler import select_command
from src.google_chat.bot_authorization import authorization

LOGGER = Logger()

def handler(event, context):
    """Handles an event from Google Chat."""
    LOGGER.info(f'Event: {json.dumps(event)}')
    text = filter_events(event)
    return response(text)

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
        text = f'Thanks for starting to chat with me {user_name}, I will be very happy to help you!\n\nThe commands I have available are:\n\n-> `/wafiprelease`\n-> `/sgiprelease`'
    elif event['type'] == 'ADDED_TO_SPACE' and 'singleUserBotDm' not in event['space'].keys():
        text = 'Thanks for adding me to "%s"!' % (event['space']['displayName'] if event['space']['displayName'] else 'this chat')
    elif event['type'] == 'MESSAGE' and 'slashCommand' not in event['message'].keys():
        text = f'Sorry {user_name}, I\'m currently accepting only slash commands!\n\n*Commands List:*\n\n-> `/wafiprelease`\n-> `/sgiprelease`'
    elif event['type'] == 'MESSAGE' and 'slashCommand' in event['message'].keys():
        text = select_command(event, user_name, user_email)
    else:
        text = 'Invalid event type'
        LOGGER.error(text)
        return text
    return text

def response(text):
    return ({
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "text": text
            })
        })
