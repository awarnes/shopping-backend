from flask import Blueprint, jsonify, request
from ..handlers import products
from ..model.product import ProductSchema

product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/product/<int:id>')
def get_product_by_id(id: int):
    return jsonify(ProductSchema().dump(products.get_product_by_id(id)))