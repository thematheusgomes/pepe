import os
import json
from src.log import Logger

LOGGER = Logger()
USER_PERMISSIONS = json.loads(os.getenv('USER_PERMISSIONS'))

def user_authorization(user_name, user_email, type):
    for user in USER_PERMISSIONS['users'][type]:
        if user_name == user['name'] and user_email == user['email']:
            LOGGER.info(f'Authorized {type} user: {json.dumps({"name": user_name, "email": user_email})}')
            return True
    LOGGER.info(f'Unauthorized {type} user: {json.dumps({"name": user_name, "email": user_email})}')
    return False
