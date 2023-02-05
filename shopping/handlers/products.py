import json
from typing import List
import users
from ..lib.connection import fetch_all, fetch_one, insert_one
from ..model.product import Product, ProductSchema

def get_product_by_id(id: int) -> Product:
    product = fetch_one("SELECT * FROM products WHERE id = :id", {"id", id})

    if product:
        return ProductSchema.load(product)
    return {}

def add_or_update_product(product: Product) -> Product | Exception:
    return insert_one(
        '''
        INSERT INTO products (name, tags, brand, sku, location)
        VALUES (:name, :tags, :brand, :sku, :location)
        ON CONFLICT (sku) DO UPDATE SET
            name = excluded.name,
            tags = excluded.tags,
            location = excluded.location;
        ''',
        {
            "name": product.name,
            "tags": json.dumps(product.tags),
            "brand": product.brand.value,
            "sku": product.sku,
            "location": json.dumps(product.location)
        }
    )

def get_products_for_user(user_id: int) -> List[Product]:
    user = users.get_user_by_id(user_id)

    products = fetch_all(
        "SELECT * FROM products WHERE id IN (:product_ids)",
        {"product_ids": user.products}
    )

    if products:
        return ProductSchema().load(products, many=True)
