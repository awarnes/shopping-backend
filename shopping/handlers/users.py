import json
from typing import List
from flask import g
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

import products
from ..lib.connection import fetch_all, fetch_one, insert_one
from ..model.product import Product
from ..model.roles import Permission, Roles, ROLE_MAP
from ..model.user import User, UserSchema

def get_users() -> List[User] | List:
    try:
        rows = fetch_all("SELECT * FROM users;")
        return UserSchema().load(rows, many=True)
    except ValidationError as error:
        print(f'Error getting users {error}')
        return []

def get_user_by_id(id: int) -> User | dict:
    user = fetch_one("SELECT * FROM users WHERE id = :id;", {"id": id})
    if user:
        return UserSchema().load(user)
    return {}

def add_or_update_user(user: User) -> User | dict:
    roles = user.roles if user.roles else [Roles.USER]
    return insert_one(
        '''
        INSERT INTO users (name, username, password, products, preferences, roles)
        VALUES (:name, :username, :password, :products, :preferences, :roles)
        ON CONFLICT (username) DO UPDATE SET
            name = excluded.name,
            password = excluded.password,
            products = excluded.products,
            preferences = excluded.preferences,
            roles = excluded.roles;
        ''',
        {
            "name": user.name,
            "username": user.username,
            "password": user.password,
            "products": json.dumps(user.products),
            "preferences": json.dumps(user.preferences),
            "roles": json.dumps(roles)
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

def add_favorite_product(product: Product) -> User:
    user: User = g.current_user

    if products.add_or_update_product(product):
        user.products.append(product.id)
        if add_or_update_user(user):
            return user
    raise Exception("Unable to add favorite product")