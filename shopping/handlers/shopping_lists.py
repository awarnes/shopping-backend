import json
from typing import List
from flask import Response, jsonify, make_response
from marshmallow import ValidationError
from . import products
from ..lib.connection import fetch_all, fetch_one, insert_one
from ..model.product import Product
from ..model.shopping_list import ShoppingList, ShoppingListSchema

def get_lists_for_user(id: int) -> ShoppingList | List:
    try:
        rows = fetch_all("SELECT * FROM lists;")
        filtered_rows = filter(lambda row: id in row['owners'], rows)
        return ShoppingListSchema().load(filtered_rows, many=True)
    except ValidationError as error:
        return make_response(jsonify({"message": error.messages}), 400)

def get_list_by_id(list_id: int) -> ShoppingList | Response:
    shopping_list = fetch_one("SELECT * FROM lists WHERE id = :id;", {"id": list_id})
    print(f"SQL LIST: {shopping_list}")
    if shopping_list:
        return ShoppingListSchema().load(shopping_list)
    return make_response(jsonify({"message": f"Unable to find list [{list_id}]"}), 404)

def create_list_for_user(user_id: int, shopping_list: ShoppingList) -> int:
    owners = set(shopping_list.owners)
    owners.add(user_id)
    return insert_one(
        """
        INSERT INTO lists (products, owners, subscribers, name)
        VALUES (:products, :owners, :subscribers, :name)
        RETURNING id;
        """,
        {
            "name": shopping_list.name,
            "products": json.dumps(shopping_list.products),
            "owners": json.dumps(list(owners)),
            "subscribers": json.dumps(shopping_list.subscribers)
        },
        returning=True
    )[0]

def update_list(shopping_list: ShoppingList) -> bool:
    return insert_one(
        '''
        UPDATE lists SET
            name = :name,
            products = :products,
            owners = :owners,
            subscribers = :subscribers
        WHERE id = :id;
        ''',
        {
            "id": shopping_list.id,
            "name": shopping_list.name,
            "products": json.dumps(shopping_list.products),
            "owners": json.dumps(shopping_list.owners),
            "subscribers": json.dumps(shopping_list.subscribers)
        }
    )

def add_products_to_list(list_id: int, products: List[Product]) -> ShoppingList | Response:
    shopping_list = get_list_by_id(list_id)
    if shopping_list:
        shopping_list.products += [product.id for product in products]
        if update_list(shopping_list):
            return shopping_list
        return make_response(jsonify({"message": f"Unable to update list [{list_id}]"}), 422)
    return make_response(jsonify({"message": f"Unable to find list [{list_id}]"}), 404)
            

def add_subscribers_to_list(list_id: int, subscribers: List[int]) -> ShoppingList | Response:
    shopping_list = get_list_by_id(list_id)
    if shopping_list:
        shopping_list.subscribers =list(set(shopping_list.subscribers + subscribers))
        if update_list(shopping_list):
            return shopping_list
        return make_response(jsonify({"message": f"Unable to update list [{list_id}]"}), 422)
    return make_response(jsonify({"message": f"Unable to find list [{list_id}]"}), 404)

def add_owners_to_list(list_id: int, owners: List[int]) -> ShoppingList | Response:
    shopping_list = get_list_by_id(list_id)
    if shopping_list:
        shopping_list.owners = list(set(shopping_list.owners + owners))
        if update_list(shopping_list):
            return shopping_list
        return make_response(jsonify({"message": f"Unable to update list [{list_id}]"}), 422)
    return make_response(jsonify({"message": f"Unable to find list [{list_id}]"}), 404)