import boto3
import json
from src.security.user_authorization import user_authorization
from src.logger import Logger

logger = Logger()

lambda_client = boto3.client('lambda')

def handle_turn_on_off_function(arguments, user_name, user_email):
    if user_authorization(user_name, user_email, type = 'dev') or user_authorization(user_name, user_email, type = 'admin'):
        event = {
            'Action': arguments[0],
            "Environment": arguments[1:-1],
            "Target": arguments[-1]
        }
        return invoke_function(event, 'tools-turn-on-off')
    return f'{user_name} you are not authorized to perform this command, please contact your administrator'

def invoke_function(event, function_name):
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(event).encode('utf-8')
        )

        payload_decoded = json.loads(response['Payload'].read().decode("utf-8"))
        payload = json.loads(payload_decoded)

        lambda_response = json.dumps({
            'statusCode': response['StatusCode'],
            'payload': payload
        })
        logger.info(f'Lambda Response: {lambda_response}')

        return payload['message']

    except Exception as e:
        logger.error(e)
