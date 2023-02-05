from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from ..handlers import shopping_lists
from ..lib.decorators import basic_authentication, authorize
from ..model.product import ProductSchema
from ..model.roles import Permission
from ..model.shopping_list import ShoppingListSchema

shopping_list_blueprint = Blueprint('shopping_list', __name__)

@shopping_list_blueprint.route('/list/<int:list_id>')
def get_list_by_id(list_id: int):
    return jsonify(ShoppingListSchema().dump(shopping_lists.get_list_by_id(list_id)))

@shopping_list_blueprint.route('/list/<int:list_id/products', methods=['POST'])
@basic_authentication
def add_products_to_list(list_id: int):
    try:
        products = ProductSchema().load(request.get_json(), many=True)
    except ValidationError as error:
        return error, 400

    return jsonify(
        ShoppingListSchema().dump(shopping_lists.add_products_to_list(list_id, products), many=True)
    )

@shopping_list_blueprint.route('/list/<int:list_id/subscribers', methods=['POST'])
@basic_authentication
def add_subscribers_to_list(list_id: int):
    try:
        subscribers = request.get_json()['subscribers']
    except KeyError as error:
        return error, 400

    return jsonify(
        ShoppingListSchema().dump(shopping_lists.add_subscribers_to_list(list_id, subscribers), many=True)
    )

@shopping_list_blueprint.route('/list/<int:list_id/owners', methods=['POST'])
@basic_authentication
@authorize(required_perms=[Permission.UPDATE_SELF_LIST, Permission.UPDATE_ANY_LIST])
def add_owners_to_list(list_id: int):
    try:
        owners = request.get_json()['owners']
    except KeyError as error:
        return error, 400

    return jsonify(
        ShoppingListSchema().dump(shopping_lists.add_owners_to_list(list_id, owners), many=True)
    )