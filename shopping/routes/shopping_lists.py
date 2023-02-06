from typing import List
from flask import Blueprint, Response, jsonify, make_response, request
from marshmallow import ValidationError

from ..handlers import shopping_lists, products
from ..lib.decorators import basic_authentication, authorize
from ..model.product import Product, ProductSchema
from ..model.roles import Permission
from ..model.shopping_list import ShoppingList, ShoppingListSchema

shopping_list_blueprint = Blueprint('shopping_list', __name__)

@shopping_list_blueprint.route('/list/<int:list_id>')
def get_list_by_id(list_id: int):
    shopping_list: ShoppingList | Response = shopping_lists.get_list_by_id(list_id)

    if isinstance(shopping_list, Response):
        return shopping_list
    return jsonify(ShoppingListSchema().dump(shopping_list))

@shopping_list_blueprint.route('/list/<int:list_id>/products', methods=['POST'])
@basic_authentication
def add_products_to_list(list_id: int):
    try:
        products: List[Product] = ProductSchema().load(request.get_json(), many=True)
    except ValidationError as error:
        return make_response(jsonify({"message": error.messages}), 400)

    shopping_list: ShoppingList | Response = shopping_lists.add_products_to_list(list_id, products)
    if isinstance(shopping_list, Response):
        return shopping_list
    return jsonify(ShoppingListSchema().dump(shopping_list))

@shopping_list_blueprint.route('/list/<int:list_id>/products')
def get_products_for_list(list_id: int):
    product_list: List[Product] | Response = products.get_products_for_list(list_id)

    if isinstance(product_list, Response):
        return product_list
    return jsonify(ProductSchema().dump(product_list, many=True))

@shopping_list_blueprint.route('/list/<int:list_id>/subscribers', methods=['POST'])
@basic_authentication
def add_subscribers_to_list(list_id: int):
    try:
        subscribers: List[int] = request.get_json()
    except KeyError as error:
        return error, 400

    shopping_list: ShoppingList | Response = shopping_lists.add_subscribers_to_list(list_id, subscribers)
    if isinstance(shopping_list, Response):
        return shopping_list
    return jsonify(ShoppingListSchema().dump(shopping_list))

@shopping_list_blueprint.route('/list/<int:list_id>/owners', methods=['POST'])
@basic_authentication
@authorize(required_perms=[Permission.UPDATE_SELF_LIST, Permission.UPDATE_ANY_LIST])
def add_owners_to_list(list_id: int):
    try:
        owners: List[int] = request.get_json()
    except KeyError as error:
        return error, 400

    shopping_list: ShoppingList | Response = shopping_lists.add_owners_to_list(list_id, owners)
    if isinstance(shopping_list, Response):
        return shopping_list
    return jsonify(ShoppingListSchema().dump(shopping_list))