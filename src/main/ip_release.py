import json
from main.util import validate_json_with_schema, allow_ip_on_waf


def handler(event, context):

    if validate_json_with_schema(event):
        changed_wafs = allow_ip_on_waf(event)['message']    
        body = {
            "message": changed_wafs,
            "input": event
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        return response
    else:
        response = {
            "statusCode":400,
            "message": "error with input JSON. Check logs for JSON Schema"
        }
        return response
