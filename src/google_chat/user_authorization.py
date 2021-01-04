import os
import json
from log import Logger

LOGGER = Logger()
USERS = json.loads(os.getenv('USERS'))

def user_authorization(user_name, user_email, type):
    for user in USERS['users'][type]:
        if user_name == user['name'] and user_email == user['email']:
            LOGGER.info(f'Authorized {type} user: {json.dumps(user)}')
            return True
        else:
            LOGGER.error(f'Unauthorized {type} user: {json.dumps({"name": user_name, "email": user_email})}')
            return False
