import json
import boto3
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from main.log import Logger

ip_sets = os.environ['ip_sets']

LOGGER = Logger()
schema = {
    "type": "object",
    "required": ["action", "location", "ip"],
    "properties" : {
        "action" : {"type" : "string"},
        "location" : {"type" : "string"},
        "ip" : {"type" : "string"},
    }
}

def validate_json_with_schema(json_input):
    try:
        validate(instance=json_input,schema=schema)
        LOGGER.info('JSON Input is valid')
        return True
    except ValidationError as exception:
        LOGGER.error(exception)
        return False

def allow_ip_on_waf(event):
    with open(ip_sets) as f:
        ip_sets_json = json.load(f)
        if 'RegionalId' in ip_sets_json[event['location']]:
            LOGGER.info('%s will perform changes on Global and Regional WAFs', event['location'])
            waf_global = boto3.client('waf')
            global_token = waf_global.get_change_token()
            response = waf_global.update_ip_set(
            IPSetId=ip_sets_json[event['location']]['GlobalId'],
            ChangeToken=global_token['ChangeToken'],
            Updates=[
                {
                    'Action': 'INSERT',
                    'IPSetDescriptor': {
                        'Type': 'IPV4',
                        'Value': event['ip']
                    }
                }
            ]
            )

            waf_regional = boto3.client('waf-regional')
            regional_token = waf_regional.get_change_token()
            response = waf_regional.update_ip_set(
            IPSetId=ip_sets_json[event['location']]['RegionalId'],
            ChangeToken=regional_token['ChangeToken'],
            Updates=[
                {
                    'Action': 'INSERT',
                    'IPSetDescriptor': {
                        'Type': 'IPV4',
                        'Value': event['ip']
                    }
                }
            ]
            )
            return {'waf': 2, 'message': 'IP added to Regional and Global WAF'}
        else:
            LOGGER.info('%s will perform changes on Global WAF', event['location'])
            waf_global = boto3.client('waf')
            global_token = waf_global.get_change_token()
            response = waf_global.update_ip_set(
            IPSetId=ip_sets_json[event['location']]['GlobalId'],
            ChangeToken=global_token['ChangeToken'],
            Updates=[
                {
                    'Action': 'INSERT',
                    'IPSetDescriptor': {
                        'Type': 'IPV4',
                        'Value': event['ip']
                    }
                }
            ]
            )
            return {'waf': 1, 'message': 'IP added to Global WAF'}