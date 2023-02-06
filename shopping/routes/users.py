from typing import List
from flask import Blueprint, Response, jsonify, make_response, request
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash

from ..lib.decorators import authorize, basic_authentication
from ..handlers import products, shopping_lists, users

from ..model.product import Product, ProductSchema
from ..model.roles import Permission
from ..model.shopping_list import ShoppingList, ShoppingListSchema
from ..model.user import User, UserSchema


user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users')
def get_users():
    user_list: List[User] | Response = users.get_users()

    if isinstance(user_list, Response):
        return user_list
    return jsonify(UserSchema().dump(user_list, many=True))

@user_blueprint.route('/user/<int:user_id>')
def get_user_by_id(user_id: int):
    user: User | Response = users.get_user_by_id(user_id)

    if isinstance(user, Response):
        return user
    return jsonify(UserSchema().dump(user))

@user_blueprint.route('/user', methods=['POST'])
def add_user():
    try:
        user: User = UserSchema().load(request.get_json())
    except ValidationError as error:
        return make_response(jsonify({"message": error.messages}), 400)

    user.password = generate_password_hash(user.password)
    user_id: int | Response = users.add_user(user)

    if isinstance(user_id, Response):
        return user_id
    return make_response(jsonify({"user_id": user_id}), 200)

# @user_blueprint.route('/login', methods=['POST'])
# def login():
#     authenticated_user = users.authenticate_user(**request.get_json())  
#     if authenticated_user:
#         return '', 204
#     return 'Authentication failed', 401

@user_blueprint.route('/user/<int:user_id>/product')
def get_products_for_user(user_id: int):
    return jsonify(ProductSchema().dump(products.get_products_for_user(user_id), many=True))

@user_blueprint.route('/user/<int:user_id>/list')
def get_lists_for_user(user_id: int):
    return jsonify(ShoppingListSchema().dump(shopping_lists.get_lists_for_user(user_id), many=True))

@user_blueprint.route('/user/<int:user_id>/list', methods=['POST'])
@basic_authentication
@authorize(required_perms=[Permission.CREATE_SELF_LIST])
def create_list_for_user(user_id: int):
    try:
        shopping_list: ShoppingList = ShoppingListSchema().load(request.get_json())
    except ValidationError as error:
        return make_response(jsonify({"message": error.messages}), 400)

    if shopping_lists.create_list_for_user(user_id, shopping_list):
        print("LIST CREATED")
        return jsonify({"message": f'List created for {user_id}'}), 200
    print("LIST FAILED")
    return jsonify({"message": 'List was not created'}), 500

@user_blueprint.route('/user/<int:user_id>', methods=['PATCH'])
@basic_authentication
@authorize(required_perms=[Permission.UPDATE_ANY_USER, Permission.UPDATE_SELF_USER])
def update_user(user_id: int):
    try:
        user: User = UserSchema().load(request.get_json())
    except ValidationError as error:
        return make_response(jsonify({"message": error.messages}), 400)
    if users.update_user(user):
        return '', 200
    return make_response(jsonify({"message": "User failed to be added"}), 500)

@user_blueprint.route('/user/<int:user_id>/product', methods=['POST'])
@basic_authentication
@authorize(required_perms=[Permission.CREATE_ANY_PRODUCT, Permission.CREATE_SELF_PRODUCT])
def add_favorite_product(user_id: int):
    try:
        product: Product = ProductSchema().load(request.get_json())
    except ValidationError as error:
        return make_response(jsonify({"message": error.messages}), 400)
    
    if users.add_favorite_product(product):
        return make_response(jsonify({"message": f'Favorite added for {user_id}'}), 200)
    return make_response(jsonify({"message": 'Product not favorited'}), 500)