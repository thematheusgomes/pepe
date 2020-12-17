# app.py

import json
from flask import Flask, request
from log import Logger
from google_chat.slash_commands.commands_handler import slash_command_handler
from google_chat.auth import authorization

LOGGER = Logger()
app = Flask(__name__)

@app.route('/google-chat', methods=['POST'])
def on_event():
    """Handles an event from Google Chat."""
    event = request.get_json()
    token = request.headers.get('Authorization').replace('Bearer ', '')
    # Check the authenticity of the token sent
    authorization(token)
    user_email = event['user']['email']
    user_name = event['user']['displayName'] if event['user']['displayName'] else 'Dear'
    LOGGER.info(f'Event: {json.dumps(event)}')
    if event['type'] == 'ADDED_TO_SPACE' and 'singleUserBotDm' not in event['space'].keys():
        text = 'Thanks for adding me to "%s"!' % (event['space']['displayName'] if event['space']['displayName'] else 'this chat')
    elif event['type'] == 'MESSAGE' and 'slashCommand' not in event['message'].keys():
        text = f'Sorry {user_name}, I\'m currently accepting only slash commands!\n\n*Commands List:*\n\n> `/iprelease`'
    elif event['type'] == 'MESSAGE' and 'slashCommand' in event['message'].keys():
        text = slash_command_handler(event, user_name, user_email)
    else:
        text = 'Invalid event type'
        LOGGER.error(text)
        return response(text)
    return response(text)

def response(text):
    return json.dumps({'text': text})
