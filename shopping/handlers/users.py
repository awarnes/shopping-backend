import json
import sqlite3
from typing import List
from flask import Response, g, jsonify, make_response
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

from . import products
from ..lib.connection import fetch_all, fetch_one, insert_one
from ..model.product import Product
from ..model.roles import Permission, Roles, ROLE_MAP
from ..model.user import User, UserSchema

def get_users() -> List[User] | Response:
    try:
        rows = fetch_all("SELECT * FROM users;")
        return UserSchema().load(rows, many=True)
    except ValidationError as error:
        return make_response(jsonify({"message": error.messages}), 400)

def get_user_by_id(user_id: int) -> User | Response:
    user = fetch_one("SELECT * FROM users WHERE id = :id;", {"id": user_id})
    print(f"USER {user}")
    if user:
        try:
            return UserSchema().load(user)
        except ValidationError as error:
            return make_response(jsonify({"message": error.messages}), 500)
    return make_response(jsonify({"message": f"Unable to find user [{user_id}]"}), 404)

def add_user(user: User) -> int | Response:
    try:
        return insert_one(
            '''
            INSERT INTO users (name, username, password, products, preferences, roles)
            VALUES (:name, :username, :password, :products, :preferences, :roles)
            RETURNING id;
            ''',
            {
                "name": user.name,
                "username": user.username,
                "password": user.password,
                "products": json.dumps(user.products),
                "preferences": json.dumps(user.preferences),
                "roles": json.dumps(user.roles)
            },
            returning=True
        )[0]
    except sqlite3.IntegrityError:
        return make_response(jsonify({"message": "Username already exists"}), 422)

def update_user(user: User) -> bool:
    return insert_one(
        '''
        UPDATE users SET
            name = COALESCE(:name, name),
            password = COALESCE(:password, password),
            products = COALESCE(:products, products),
            preferences = COALESCE(:preferences, preferences),
            roles = COALESCE(:roles, roles);
        ''',
        {
            "name": user.name,
            "username": user.username,
            "password": user.password,
            "products": json.dumps(user.products),
            "preferences": json.dumps(user.preferences),
            "roles": json.dumps(user.roles)
        }
    )

def authenticate_user(username: str, password: str) -> User | bool:
    user = fetch_one("SELECT * FROM users WHERE username = :username;", {"username": username})
    if user:
        if check_password_hash(user["password"], password):
            return UserSchema().load(user)
        return False

def get_user_permissions(user_id: int) -> List[Permission]:
    user_roles = fetch_one("SELECT roles FROM users WHERE id = :user_id;", {"user_id": user_id})
    if not user_roles:
        return None
    permissions = []
    for role in user_roles['roles']:
        permissions += ROLE_MAP[role]
    if Permission.ALL in permissions:
        permissions = [e.value for e in Permission]
    return permissions

def add_favorite_product(product: Product) -> User | Response:
    user: User = g.current_user
    print(f"AF USER: {user}")
    print(f"AF PRODUCT: {product}")
    if product_id := products.add_or_update_product(product):
        user.products.append(product_id[0])
        print(f"AF post USER: {user}")
        if update_user(user):
            return user
        return make_response(jsonify({"message": f"Unable to update product [{product.id}]"}), 422)
    return make_response(jsonify({"message": f"Unable to update user [{user.id}]"}), 422)