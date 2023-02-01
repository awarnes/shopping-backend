from typing import List
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

from ..lib.connection import fetch_all, fetch_one, insert_one
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
    return insert_one(
        "INSERT INTO users (name, username, password) VALUES (:name, :username, :password);",
        {"name": user.name, "username": user.username, "password": user.password}
    )

def authenticate_user(username: str, password: str) -> User | bool:
    user = fetch_one("SELECT * FROM users WHERE username = :username;", {"username": username})
    if user:
        if check_password_hash(user["password"], password):
            return UserSchema().load(user)
        return False
