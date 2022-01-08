import json
from src.logger import Logger
from src.security.bot_authentication import authentication
from src.commands.handle_commands import select_command
from src.messages.send_messages import send_message_to_space

logger = Logger()

def handler(event, context):
    """Handles an event from Google Chat."""
    logger.info(f'Event: {json.dumps(event)}')

    if 'headers' not in event and 'resource' in event and event['resource'] == 'cloudwatch events':
        message = select_command(event, event['user']['displayName'], event['user']['email'])
        return send_message_to_space(message)

    message = bot_handler(event)

    logger.info('Sending message to Google Chat')
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "text": message
        })
    }

def bot_handler(event):

    token = event['headers']['Authorization'].replace('Bearer ', '')
    authentication(token)

    event = json.loads(event['body'])
    user_email = event['user']['email']
    user_name = event['user']['displayName'] if event['user']['displayName'] else 'Dear'
    logger.info(f'Name: {user_name}, Email: {user_email}')
    if event['type'] == 'ADDED_TO_SPACE' and 'singleUserBotDm' in event['space'].keys():
        logger.info(f'User {user_name} starts a conversation with Pepe')
        return f'Thanks for starting to chat with me {user_name}, I will be very happy to help you!\n\nThe commands I have available are:\n\n- `/iprelease`\n- `/sgipupdate`\n- `/turnonoff`'
    elif event['type'] == 'ADDED_TO_SPACE' and 'singleUserBotDm' not in event['space'].keys():
        logger.info('Pepe was added to space "%s"' % (event['space']['displayName'] if event['space']['displayName'] else 'unknown'))
        return 'Thanks for adding me to "%s"!' % (event['space']['displayName'] if event['space']['displayName'] else 'this space')
    elif event['type'] == 'MESSAGE' and 'slashCommand' not in event['message'].keys():
        return f'Sorry {user_name}, I\'m currently accepting only slash commands!\n\n*Commands List:*\n\n- `/iprelease`\n- `/sgipupdate`\n- `/turnonoff`\n\nIf the problem persists, try typing slash "/" then wait a while, a list of commands should appear, then select the command you want.'
    elif event['type'] == 'MESSAGE' and 'slashCommand' in event['message'].keys():
        return select_command(event, user_name, user_email)
    else:
        logger.error('Invalid event type')
        return 'Invalid event type'
