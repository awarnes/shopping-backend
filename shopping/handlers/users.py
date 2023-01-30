from marshmallow import ValidationError
from ..model.connection import fetch_all
from ..model.user import UserSchema

def get_users():
    try:
        rows = fetch_all("SELECT * FROM users;")
        return UserSchema().load(rows, many=True)
    except ValidationError as error:
        print(f'Error getting users {error}')
        return []