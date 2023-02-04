from flask import Flask
from shopping.routes.users import user_blueprint
from shopping.routes.shopping_lists import shopping_list_blueprint

app = Flask(__name__)

app.register_blueprint(user_blueprint)
app.register_blueprint(shopping_list_blueprint)
