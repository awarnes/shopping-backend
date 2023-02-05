import requests
from flask import g
from .authenticate import authenticate

GET_STORES_URL = 'https://api.kroger.com/v1/locations'
API_401_ERROR = 'API-401'

def get_stores(zip_code: str, radius: int):
    '''
    curl -X GET \
        'https://api.kroger.com/v1/locations' \
        -H 'Accept: application/json' \
        -H 'Authorization: Bearer {{TOKEN}}'
    '''

    try:
        headers = {'Authorization': f"Bearer {g.KROGER_ACCESS_TOKEN}"}
    except AttributeError:
        # First time start up requires g to be populated
        authenticate()
        headers = {'Authorization': f"Bearer {g.KROGER_ACCESS_TOKEN}"}

    params = {'filter.zipCode.near': zip_code, 'filter.radiusInMiles': radius}

    response = requests.get(GET_STORES_URL, headers=headers, params=params).json()

    if 'error' in response and API_401_ERROR in response["error"]:
        authenticate()
        return get_stores(zip_code, radius)

    return response
