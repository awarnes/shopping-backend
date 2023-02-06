import json
from typing import List
from flask import Response, jsonify, make_response
from . import users
from . import shopping_lists
from ..lib.connection import fetch_all, fetch_one, insert_one
from ..model.product import Product, ProductSchema

def get_product_by_id(product_id: int) -> Product | Response:
    product = fetch_one("SELECT * FROM products WHERE id = :id", {"id": product_id})

    if product:
        return ProductSchema().load(product)
    return make_response(jsonify({"message": f"Unable to find product [{product_id}]"}), 404)

def add_or_update_product(product: Product) -> Product | Exception:
    return insert_one(
        '''
        INSERT INTO products (name, tags, brand, sku, location)
        VALUES (:name, :tags, :brand, :sku, :location)
        ON CONFLICT (brand, sku) DO UPDATE SET
            name = excluded.name,
            tags = excluded.tags,
            location = excluded.location
        RETURNING id;
        ''',
        {
            "name": product.name,
            "tags": json.dumps(product.tags),
            "brand": product.brand.value,
            "sku": product.sku,
            "location": json.dumps(product.location)
        },
        returning=True
    )

def get_products_for_user(user_id: int) -> List[Product]:
    user = users.get_user_by_id(user_id)
    user_product_ids = ','.join([str(prod_id) for prod_id in user.products])
    products = fetch_all(
        "SELECT * FROM products WHERE id IN (:product_ids)",
        {"product_ids": user_product_ids}
    )

    if products:
        return ProductSchema().load(products, many=True)

def get_products_for_list(list_id: int) -> List[Product]:
    shopping_list = shopping_lists.get_list_by_id(list_id)
    list_product_ids = ','.join([str(prod_id) for prod_id in shopping_list.products])
    products = fetch_all(
        "SELECT * FROM products WHERE id IN (:product_ids)",
        {"product_ids": list_product_ids}
    )

    if products:
        return ProductSchema().load(products, many=True)
