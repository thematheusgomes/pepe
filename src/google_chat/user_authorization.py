import json
from log import Logger

LOGGER = Logger()
USERS = {
    "users": {
        "admin": [
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
        ],
        "dev": [
            {
                "name": "Murilo Veiga",
                "email": "murilo.veiga@boomcredit.net"
            },
            {
                "name": "Jose Luis Trinidad del Real",
                "email": "jose.real@boomcredit.net"
            }
        ]
    }
}

def user_authorization(user_name, user_email, type):
    for user in USERS['users'][type]:
        if user_name == user['name'] and user_email == user['email']:
            LOGGER.info(f'Authorized {type} user: {json.dumps(user)}')
            return True
        else:
            LOGGER.error(f'Unauthorized {type} user: {json.dumps({"name": user_name, "email": user_email})}')
            return False
