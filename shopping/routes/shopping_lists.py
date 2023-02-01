from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from ..handlers import shopping_lists
from ..lib.decorators import basic_authentication
from ..model.shopping_list import ShoppingList, ShoppingListSchema

shopping_list_blueprint = Blueprint('shopping_list', __name__)

# @list_blueprint.route('')
