from ...lib.connection import fetch_all

def get_stores(zip_code: str, radius: int):
    return fetch_all("SELECT * FROM stores WHERE brand='TRADER_JOES';")