from dataclasses import dataclass
from typing import Optional
from marshmallow import Schema, fields, post_load
from werkzeug.security import generate_password_hash

class User:
    def __init__(
        self,
        username: str,
        password: str,
        name: Optional[str],
        id: Optional[int] = None,
        created: Optional[str] = None,
        updated: Optional[str] = None
    ):
        self.name = name
        self.username = username
        if len(password.split('$')) == 3:
            self.password = password
        else:
            self.password = generate_password_hash(password)
        self.id = id
        self.created = created
        self.updated = updated

class UserSchema(Schema):
    name = fields.Str()
    username = fields.Str()
    password = fields.Str()
    id = fields.Number(allow_none=True)
    created = fields.DateTime(allow_none=True)
    updated = fields.DateTime(allow_none=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
