from .graphql import make_query

PRODUCT_QUERY = '''
    query SearchProducts($search_term: String, $page_size: Int, $current_page: Int, $location: String, $availability: String, $published: String, $sku: String) {
        products(
            search: $search_term
            filter: {store_code: {eq: $location}, published: {eq: $published}, availability: {match: $availability}, sku: {eq: $sku}}
            pageSize: $page_size
            currentPage: $current_page
        ) {
            items {
                availability
                allergens {
                    ingredient
                }
                item_title
                item_description
                product_label
                promotion
                retail_price
                sku
                special_price
                special_to_date
                special_from_date
                store_specific_info {
                    availability
                    retail_price
                    store_code
                }
                thumbnail {
                    url
                    label
                }
            }
            page_info {
                current_page
                page_size
                total_pages
            }
        }
    }
'''

def search_for_product(search_term: str, location: str = None):
    variables = {
        'availability': '1',
        'published': '1',
        'page_size': 10,
        'current_page': 1,
        'location': location,
        'search_term': search_term,
        # 'sku': '055005'
    }

    response = make_query(PRODUCT_QUERY, variables=variables)
    
    return response