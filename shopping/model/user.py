from typing import List, Optional
from marshmallow import Schema, fields, post_load
from .preferences import Preferences, PreferencesSchema
from .roles import Roles

class User:
    def __init__(
        self,
        username: str,
        password: str,
        name: Optional[str],
        preferences: Optional[Preferences] = None,
        products: Optional[List[int]] = None,
        id: Optional[int] = None,
        roles: Optional[List[Roles]] = None,
        created: Optional[str] = None,
        updated: Optional[str] = None
    ):
        self.name = name
        self.username = username
        self.password = password
        self.preferences = preferences
        self.products = products
        self.id = id
        self.roles = roles
        self.created = created
        self.updated = updated

class UserSchema(Schema):
    name = fields.Str()
    username = fields.Str()
    password = fields.Str()
    preferences = fields.Nested(PreferencesSchema)
    products = fields.List(fields.Int(), allow_none=True)
    id = fields.Int(allow_none=True)
    roles = fields.List(fields.Enum(enum=Roles), allow_none=True)
    created = fields.DateTime(allow_none=True)
    updated = fields.DateTime(allow_none=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
