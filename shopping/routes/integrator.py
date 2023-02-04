from flask import Blueprint, jsonify, request
from ..integrations import Integrator, get_integrator

integrator_blueprint = Blueprint('store_integrator', __name__)

@integrator_blueprint.route('/integrator/<string:integrator>/stores')
def get_stores(integrator: str):
    integrator = Integrator(integrator.upper())
    zip_code = request.args.get('zip_code', default='97216')
    radius = request.args.get('radius', default=10)
    return jsonify(get_integrator(integrator).get_stores(zip_code=zip_code, radius=radius))

@integrator_blueprint.route('/integrator/<string:integrator>/products')
def search_for_product(integrator: str):
    integrator = Integrator(integrator.upper())
    search_term = request.args.get('search_term', default=None)
    location = request.args.get('location', default=None)
    return jsonify(get_integrator(integrator).search_for_product(search_term=search_term, location=location))