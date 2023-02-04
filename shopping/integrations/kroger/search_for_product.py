import requests
from flask import g
from .authenticate import authenticate

KROGER_SEARCH_URL = 'https://api.kroger.com/v1/products'
API_401_ERROR = 'API-401'

def search_for_product(search_term: str, location: str = None):
    '''
    curl -X GET \
        'https://api.kroger.com/v1/products?filter.brand={{BRAND}}&filter.term={{TERM}}&filter.locationId={{LOCATION_ID}}' \
        -H 'Accept: application/json' \
        -H 'Authorization: Bearer {{TOKEN}}'
    '''

    try:
        headers = {'Authorization': f'Bearer {g.KROGER_ACCESS_TOKEN}'}
    except AttributeError:
        authenticate()
        headers = {'Authorization': f'Bearer {g.KROGER_ACCESS_TOKEN}'}
    
    params = {'filter.term': search_term, 'filter.locationId': location or g.current_user.kroger.preferred_location}

    response = requests.get(KROGER_SEARCH_URL, headers=headers, params=params).json()

    if "error" in response and API_401_ERROR in response["error"]:
        authenticate()
        return search_for_product(search_term, location)
    
    return response