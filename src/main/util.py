import json
import boto3
import os
import urllib
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from main.log import Logger

BOT_TOKEN = os.environ["BOT_TOKEN"]
SLACK_URL = os.environ["SLACK_URL"]
LOGGER = Logger()

def response_builder(response_code, message):
    body = {
        "message": message,
    }

    response = {
        "statusCode": response_code,
        "body": body
    }
    return response

def send_slack_message(channel_id,message):
    try:
        data = urllib.parse.urlencode(
                (
                    ("token", BOT_TOKEN),
                    ("channel", channel_id),
                    ("text", message)
                )
            )
        data = data.encode("ascii")

        request = urllib.request.Request(
            SLACK_URL, 
            data=data, 
            method="POST"
        )

        request.add_header(
            "Content-Type", 
            "application/x-www-form-urlencoded"
        )

        urllib.request.urlopen(request).read()
        return True
    except Exception as exception:
        LOGGER.error(exception)
        return False