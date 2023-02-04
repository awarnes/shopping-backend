import json
import os
import requests
from base64 import b64encode
from flask import g

SECRETS_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secrets.json')

def get_secrets():
    with open(SECRETS_FILE_PATH) as secrets:
        return json.load(secrets)

GET_TOKEN_URL = 'https://api.kroger.com/v1/connect/oauth2/token'

AUTHORIZATION_SCOPES = ['product.compact']

def authenticate():
    '''
    curl -X POST \
        'https://api.kroger.com/v1/connect/oauth2/token' \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        -H 'Authorization: Basic {{base64(“CLIENT_ID:CLIENT_SECRET”)}}' \
        -d 'grant_type=client_credentials&scope={{SCOPE}}'
    '''

    client_auth = get_secrets()

    basic_auth = f"{client_auth['client_id']}:{client_auth['client_secret']}"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'''Basic {b64encode(bytes(basic_auth, "utf-8")).decode()}'''
    }

    data = {
        'grant_type': 'client_credentials',
        'scope': ','.join(AUTHORIZATION_SCOPES)
    }

    r = requests.post(GET_TOKEN_URL, data=data, headers=headers)

    g.KROGER_ACCESS_TOKEN = r.json()['access_token']
