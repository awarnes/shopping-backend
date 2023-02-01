from flask import Flask
from shopping.routes.users import user_blueprint


app = Flask(__name__)

app.register_blueprint(user_blueprint)
# app.register_blueprint(other_blueprint)
