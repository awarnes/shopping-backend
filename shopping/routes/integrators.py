from flask import Blueprint, g, jsonify, request
from ..lib.decorators import basic_authentication
from ..model.brand import Brand
from ..integrations import get_integrator

integrator_blueprint = Blueprint('store_integrator', __name__)

@integrator_blueprint.route('/integrator/<string:integrator>/stores')
def get_stores(integrator: str):
    integrator: Brand = Brand(integrator.upper())
    zip_code: str = request.args.get('zip_code', default='97216')
    radius: int = request.args.get('radius', default=10)
    return jsonify(get_integrator(integrator).get_stores(zip_code=zip_code, radius=radius))

@integrator_blueprint.route('/integrator/<string:integrator>/products')
@basic_authentication
def search_for_product(integrator: str):
    integrator: Brand = Brand(integrator.upper())
    search_term: str = request.args.get('search_term', default=None)
    location: str = request.args.get('location', default=g.current_user.get_preferred_store(integrator))
    return jsonify(get_integrator(integrator).search_for_product(search_term=search_term, location=location))