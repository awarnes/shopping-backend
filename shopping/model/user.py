from dataclasses import dataclass
from marshmallow import Schema, fields, post_load

@dataclass
class User:
    name: str
    username: str
    id: int
    created: str
    updated: str

class UserSchema(Schema):
    name = fields.Str()
    username = fields.Str()
    id = fields.Number()
    created = fields.DateTime()
    updated = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

