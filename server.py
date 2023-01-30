from flask import Flask
from shopping.routes import ROUTES

app = Flask(__name__)

for (url, options) in ROUTES.items():
    app.add_url_rule(url, **options)