import json
from src.log import Logger
from src.bot.messages.send_messages import send_message_to_rooms
from src.bot.bot_authorization import authorization
from src.bot.slash_commands.commands_handler import select_command

LOGGER = Logger()

def handler(event, context):
    """Handles an event from Google Chat."""
    LOGGER.info(f'Event: {json.dumps(event)}')
    if 'headers' not in event and 'resource' in event and event['resource'] == 'cloudwatch events':
        message = select_command(event, event['user']['displayName'], event['user']['email'])
        return send_message_to_rooms(message)
    return response(bot_handler(event))

def bot_handler(event):
    token = event['headers']['Authorization'].replace('Bearer ', '')
    authorization(token)
    event = json.loads(event['body'])
    user_email = event['user']['email']
    user_name = event['user']['displayName'] if event['user']['displayName'] else 'Dear'
    if event['type'] == 'ADDED_TO_SPACE' and 'singleUserBotDm' in event['space'].keys():
        LOGGER.info(f'User {user_name} starts a conversation with Pepe')
        return f'Thanks for starting to chat with me {user_name}, I will be very happy to help you!\n\nThe commands I have available are:\n\n-> `/iprelease`\n-> `/sgipupdate`'
    elif event['type'] == 'ADDED_TO_SPACE' and 'singleUserBotDm' not in event['space'].keys():
        LOGGER.info('Pepe was added to room "%s"' % (event['space']['displayName'] if event['space']['displayName'] else 'unknown'))
        return 'Thanks for adding me to "%s"!' % (event['space']['displayName'] if event['space']['displayName'] else 'this chat')
    elif event['type'] == 'MESSAGE' and 'slashCommand' not in event['message'].keys():
        return f'Sorry {user_name}, I\'m currently accepting only slash commands!\n\n*Commands List:*\n\n-> `/iprelease`\n-> `/sgipupdate`\n\nIf the problem persists, try typing slash "/" then select the command you want from the command list that will appear.'
    elif event['type'] == 'MESSAGE' and 'slashCommand' in event['message'].keys():
        return select_command(event, user_name, user_email)
    else:
        LOGGER.error('Invalid event type')
        return 'Invalid event type'

def response(message):
    LOGGER.info('Sending message to Google Chat')
    return ({
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "text": message
            })
        })
