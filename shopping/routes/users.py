from flask import Blueprint, jsonify, make_response, request
from marshmallow import ValidationError

from ..lib.decorators import basic_authentication
from ..handlers import shopping_lists, users
from ..model.user import UserSchema
from ..model.shopping_list import ShoppingListSchema

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users')
def get_users():
    return jsonify(UserSchema().dump(users.get_users(), many=True))

@user_blueprint.route('/user/<int:id>')
def get_user_by_id(id: int):
    return jsonify(UserSchema().dump(users.get_user_by_id(id)))

@user_blueprint.route('/user', methods=['POST'])
def add_user():
    try:
        user = UserSchema().load(request.get_json())
    except ValidationError as error:
        return error, 400

    if users.add_user(user):
        return '', 200
    return make_response(jsonify({"message": "User failed to be added"}), 500)

# @user_blueprint.route('/login', methods=['POST'])
# def login():
#     authenticated_user = users.authenticate_user(**request.get_json())  
#     if authenticated_user:
#         return '', 204
#     return 'Authentication failed', 401

@user_blueprint.route('/user/<int:id>/list')
def get_lists_for_user(id: int):
    return jsonify(ShoppingListSchema().dump(shopping_lists.get_lists_for_user(id), many=True))

@user_blueprint.route('/user/<int:id>/list', methods=['POST'])
@basic_authentication
def create_list_for_user(id: int):
    try:
        shopping_list = ShoppingListSchema().load(request.get_json())
    except ValidationError as error:
        return error, 400

    if shopping_lists.create_list_for_user(id, shopping_list):
        return make_response(jsonify({"message": ''}), 200)
    return make_response(jsonify({"message": 'List was not created'}), 500)