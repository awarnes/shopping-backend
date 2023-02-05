import requests
from .queries import PRODUCT_QUERY
from ..base_integrator import BaseIntegrator
from ...lib.connection import fetch_all

class TraderJoes(BaseIntegrator):
    graphql_endpoint: str = 'https://www.traderjoes.com/api/graphql'

    def get_stores(self, zip_code: str, radius: int):
        return fetch_all("SELECT * FROM stores WHERE brand='TRADER_JOES';")

    def make_query(self, query: str, variables: dict) -> dict:
        headers = {'Content-Type': 'application/json'}

        response = requests.post(self.graphql_endpoint, headers=headers, json={'query': query, 'variables': variables})

        return response.json()

    def search_for_product(self, search_term: str, location: str = None):
        variables = {
            'availability': '1',
            'published': '1',
            'page_size': 10,
            'current_page': 1,
            'location': location,
            'search_term': search_term,
            # 'sku': '055005'
        }

        response = self.make_query(PRODUCT_QUERY, variables=variables)
        
        return response