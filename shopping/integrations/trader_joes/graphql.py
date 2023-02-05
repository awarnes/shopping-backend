import requests

GRAPHQL_ENDPOINT = 'https://www.traderjoes.com/api/graphql'

def make_query(query: str, variables: dict) -> dict:
    headers = {'Content-Type': 'application/json'}

    response = requests.post(GRAPHQL_ENDPOINT, headers=headers, json={'query': query, 'variables': variables})

    return response.json()
