import os
import json
import gzip
from base64 import b64decode
from httplib2 import Http
from src.google_chat_alerts.cards import CardMessages as card
from src.log import Logger

HUND_WEBHOOK = os.getenv('HUND_WEBHOOK')
AWS_WEBHOOK = os.getenv('AWS_WEBHOOK')

LOGGER = Logger()

def hund_alerts_handler(event):
    event = json.loads(event['body'])
    component_id = event['event']['contexts']['component']['id']
    componant_name = event['event']['contexts']['component']['name']
    kind = event['event']['kind']
    LOGGER.info(f'{componant_name} has {kind}')
    if kind == 'degraded':
        color = '#E74C3C'
        message = f'<b>{componant_name}</b> has gone down.'
        hund_message = card.health_check_alert(component_id, kind, color, message)
        send_message(HUND_WEBHOOK ,hund_message)
    elif kind == 'restored':
        color = '#2ECC71'
        began_timestamp = int(event['event']['eventable']['began_at'])
        ended_timestamp = int(event['event']['eventable']['ended_at'])
        interval_timestamp = (ended_timestamp - began_timestamp)/60
        message = f'<b>{componant_name}</b> is back online.<br>It was down for <b>{round(interval_timestamp)}</b> minutes.'
        hund_message = card.health_check_alert(component_id, kind, color, message)
        send_message(HUND_WEBHOOK, hund_message)
    else:
        LOGGER.error('Invalid type of Hundio status')

def awslogs_handler(event):
    payload = awslogs_decode(event)
    logGroup = payload['logGroup']
    filterName = payload['subscriptionFilters'][0]
    count = 0
    for event in payload['logEvents']:
        count += 1
    bot_message = card.awslogs_exceptions(logGroup, filterName, str(count))
    send_message(AWS_WEBHOOK ,bot_message)

def awslogs_decode(event):
    cw_data = event['awslogs']['data']
    compressed_payload = b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)
    return payload

def send_message(webhook, bot_message):
    http_obj = Http()
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    LOGGER.info(f'Message to be sent: {json.dumps(bot_message)}')
    try:
        response = http_obj.request(
            uri=webhook,
            method='POST',
            headers=message_headers,
            body=json.dumps(bot_message),
        )
        LOGGER.info('Message sent successfully')
        LOGGER.info(response)
    except Exception as e:
        LOGGER.error(e)
