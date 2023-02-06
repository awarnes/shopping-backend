class UnimplementedException(Exception):
    pass

class BaseIntegrator:
    def get_stores(self, zip_code: str, radius: int):
        raise UnimplementedException("Get Stores Not Implemented")

    def search_for_product(self, search_term: str, location: str):
        raise UnimplementedException("Search For Product Not Implemented")
