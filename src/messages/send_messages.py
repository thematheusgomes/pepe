import os
from json import dumps
from httplib2 import Http
from src.logger import Logger

logger = Logger()
WEBHOOK = os.getenv('PEPE_WEBHOOK')

def send_message_to_space(message):
    http_obj = Http()
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    try:
        response = http_obj.request(
            uri=WEBHOOK,
            method='POST',
            headers=message_headers,
            body=dumps({'text': message})
        )
        logger.info('Message sent successfully')
        logger.info(f'Response: {response}')
    except Exception as e:
        logger.error(e)
