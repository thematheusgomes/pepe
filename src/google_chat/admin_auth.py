import json
from log import Logger

LOGGER = Logger()
ADMIN_USERS = {
    "users": [
        {
            "name": "Matheus Gomes",
            "email": "matheus.gomes@boomcredit.net"
        },
        {
            "name": "Song Kim",
            "email": "song@boomcredit.net"
        },
        {
            "name": "Joaquim Silveira",
            "email": "joaquim.silveira@boomcredit.net"
        }
    ]
}

def admin_authorization(user_name, user_email):
    for user in ADMIN_USERS['users']:
        if user_name == user['name'] and user_email == user['email']:
            LOGGER.info(f'Authorized admin user: {json.dumps(user)}')
            return True
        else:
            LOGGER.error(f'Unauthorized admin user: {json.dumps({"name": user_name, "email": user_email})}')
            return False
