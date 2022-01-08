import os
import json
from src.logger import Logger

logger = Logger()
USER_PERMISSIONS = json.loads(os.getenv('USER_PERMISSIONS'))

def user_authorization(user_name, user_email, type):
    for user in USER_PERMISSIONS['users'][type]:
        if user_name == user['name'] and user_email == user['email']:
            logger.info(f'Authorized {type} user: {json.dumps({"name": user_name, "email": user_email})}')
            return True
    logger.info(f'Unauthorized {type} user: {json.dumps({"name": user_name, "email": user_email})}')
    return False
