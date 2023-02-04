from base64 import b64decode
from functools import wraps
from typing import List

from flask import g, jsonify, make_response, request

from ..handlers.users import authenticate_user, get_user_permissions
from ..model.roles import Permission, verify_permission

def basic_authentication(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        basic_auth = None
        if 'Authorization' in request.headers:
            basic_auth = request.headers['Authorization']
        if not basic_auth:
            return make_response(jsonify({"message": "Basic authentication is missing", "code": 401}), 401)
        decoded = b64decode(bytes(basic_auth.split('Basic ')[1], 'utf-8')).decode()
        username, password = decoded.split(':')
        current_user = authenticate_user(username, password)
        if not current_user:
            return make_response(jsonify({"message": "Invalid username or password", "code": 401}), 401)
        g.current_user = current_user
        return func(*args, **kwargs)
    return decorator

def authorize(required_perms: List[Permission]):
    def decorator_authorize(func):    
        @wraps(func)
        def wrapper_authorize(*args, **kwargs):
            authorized = False
            user_perms = get_user_permissions(kwargs['user_id'])
            if not user_perms:
                return make_response(jsonify({"message": "User not found", "code": 404}), 404)
            if len(set(required_perms).difference(set(user_perms))) == 0:
                for perm in required_perms:
                    authorized = verify_permission(perm, *args, **kwargs)
            if authorized:
                return func(*args, **kwargs)
            return make_response(jsonify({"message": "Unauthorized", "code": 401}), 401)
        return wrapper_authorize
    return decorator_authorize
