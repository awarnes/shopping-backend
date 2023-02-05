from flask import Flask
from shopping.routes.integrators import integrator_blueprint
from shopping.routes.products import product_blueprint
from shopping.routes.shopping_lists import shopping_list_blueprint
from shopping.routes.users import user_blueprint

app = Flask(__name__)

app.register_blueprint(integrator_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(shopping_list_blueprint)
app.register_blueprint(user_blueprint)
