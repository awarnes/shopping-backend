from base64 import b64decode
from functools import wraps
from flask import g, jsonify, make_response, request
from ..handlers.users import authenticate_user

def basic_authentication(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        basic_auth = None
        if 'Authorization' in request.headers:
            basic_auth = request.headers['Authorization']
        if not basic_auth:
            return make_response(jsonify({"message": "Basic authentication is missing"}), 401)
        decoded = b64decode(bytes(basic_auth.split('Basic ')[1], 'utf-8')).decode()
        username, password = decoded.split(':')
        current_user = authenticate_user(username, password)
        if not current_user:
            return make_response(jsonify({"message": "Invalid username or password"}), 401)
        g.current_user = current_user
        return f(*args, **kwargs)
    return decorator
