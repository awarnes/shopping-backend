import json
from typing import List
from flask import jsonify, make_response
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

from ..lib.connection import fetch_all, fetch_one, insert_one
from ..model.roles import Permission, Roles, ROLE_MAP
from ..model.user import User, UserSchema

def get_users() -> List[User] | List:
    try:
        rows = fetch_all("SELECT * FROM users;")
        return UserSchema().load(rows, many=True)
    except ValidationError as error:
        print(f'Error getting users {error}')
        return []

def get_user_by_id(id) -> User | dict:
    user = fetch_one("SELECT * FROM users WHERE id = :id;", {"id": id})
    if user:
        return UserSchema().load(user)
    return {}

def add_user(user: User) -> User | dict:
    roles = user.roles if user.roles else [Roles.USER]
    return insert_one(
        "INSERT INTO users (name, username, password, roles) VALUES (:name, :username, :password, :roles);",
        {"name": user.name, "username": user.username, "password": user.password, "roles": json.dumps(roles)}
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