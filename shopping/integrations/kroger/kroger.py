import json
import os
import requests
from base64 import b64encode
from dataclasses import dataclass, field
from typing import List
from ..base_integrator import BaseIntegrator

SECRETS_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secrets.json')

class Kroger(BaseIntegrator):
    get_products_url: str = 'https://api.kroger.com/v1/products'
    get_stores_url: str = 'https://api.kroger.com/v1/locations'
    get_token_url: str = 'https://api.kroger.com/v1/connect/oauth2/token'
    
    def __init__(self):
        self.authorization_scopes: List[str] = ['product.compact']
        self.api_401_error: str = 'API-401'
        self.authenticate()

    def authenticate(self):
        client_auth = self.get_secrets()
        basic_auth = f"{client_auth['client_id']}:{client_auth['client_secret']}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'''Basic {b64encode(bytes(basic_auth, "utf-8")).decode()}'''
        }
        data = {
            'grant_type': 'client_credentials',
            'scope': ','.join(self.authorization_scopes)
        }
        r = requests.post(self.get_token_url, data=data, headers=headers)

        self.accessToken = r.json()['access_token']

    def get_secrets(self):
        with open(SECRETS_FILE_PATH) as secrets:
            return json.load(secrets)
        
    def get_stores(self, zip_code: str, radius: int):
        '''
        curl -X GET \
            'https://api.kroger.com/v1/locations' \
            -H 'Accept: application/json' \
            -H 'Authorization: Bearer {{TOKEN}}'
        '''

        try:
            headers = {'Authorization': f"Bearer {self.accessToken}"}
        except AttributeError:
            # First time start up requires g to be populated
            self.authenticate()
            headers = {'Authorization': f"Bearer {self.accessToken}"}

        params = {'filter.zipCode.near': zip_code, 'filter.radiusInMiles': radius}

        response = requests.get(self.get_stores_url, headers=headers, params=params).json()

        if 'error' in response and self.api_401_error in response["error"]:
            self.authenticate()
            return self.get_stores(zip_code, radius)

        return response
    
    def search_for_product(self, search_term: str, location: str = None):
        '''
        curl -X GET \
            'https://api.kroger.com/v1/products?filter.brand={{BRAND}}&filter.term={{TERM}}&filter.locationId={{LOCATION_ID}}' \
            -H 'Accept: application/json' \
            -H 'Authorization: Bearer {{TOKEN}}'
        '''

        if not self.accessToken:
            self.authenticate()

        headers = {'Authorization': f'Bearer {self.accessToken}'}
        
        params = {
            'filter.term': search_term,
            'filter.locationId': location,
            # 'filter.productId': '0000000093283'
        }

        response = requests.get(self.get_products_url, headers=headers, params=params).json()

        if "error" in response and self.api_401_error in response["error"]:
            self.authenticate()
            return self.search_for_product(search_term, location)
        
        return response