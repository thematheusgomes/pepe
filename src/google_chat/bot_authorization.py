import os
import sys
from oauth2client import client
from log import Logger

LOGGER = Logger()

# Bearer Tokens received by bots will always specify this issuer.
CHAT_ISSUER = 'chat@system.gserviceaccount.com'

# Url to obtain the public certificate for the issuer.
PUBLIC_CERT_URL_PREFIX = 'https://www.googleapis.com/service_accounts/v1/metadata/x509/'

# Intended audience of the token, which will be the project number of the bot.
AUDIENCE = os.getenv('AUDIENCE')

# Get this value from the request's Authorization HTTP header.
# For example, for 'Authorization: Bearer AbCdEf123456' use 'AbCdEf123456'.
def authorization(BEARER_TOKEN):
    try:
        # Verify valid token, signed by CHAT_ISSUER, intended for a third party.
        token = client.verify_id_token(
        BEARER_TOKEN, AUDIENCE, cert_uri=PUBLIC_CERT_URL_PREFIX + CHAT_ISSUER)
        if token['iss'] != CHAT_ISSUER:
            sys.exit('Invalid issuee')
    except:
        sys.exit('Invalid token')

    # Token originates from Google and is targeted to a specific client.
    LOGGER.info('The bot token is valid')
