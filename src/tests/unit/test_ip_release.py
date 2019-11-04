from main.ip_release import ip_release_handler
import pytest

invalid_json = {
    "command": "waf",
    "location": "Brasil",
    "ip": "169.254.169.254/32" 
}

valid_json = {
    "action": "waf",
    "location": "br",
    "ip": "169.254.169.254/32" 
}
def test_ip_handler_invalid_json():
    assert ip_release_handler(invalid_json) == {'action': 'waf', 'message': 'Error with JSON'}, f'''
        #ip_release_handler({invalid_json}) should return False
    '''

def test_ip_handler_valid_json():
    assert ip_release_handler(valid_json) == {'action': 'waf', 'message': 'IP {} allowed on WAF'.format(valid_json['ip'])}, f'''
        #ip_release_handler({valid_json}) should return True
    '''