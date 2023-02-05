from dataclasses import dataclass
from typing import List, Optional
from marshmallow import Schema, fields, post_load

class ShoppingList:
    def __init__(
        self,
        products: List[int],
        owners: List[int],
        subscribers: Optional[List[int]],
        name: Optional[str] = None,
        id: Optional[int] = None,
        created: Optional[str] = None,
        updated: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.products = products
        self.owners = owners
        self.subscribers = subscribers
        self.created = created
        self.updated = updated

class ShoppingListSchema(Schema):
    id = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)
    products = fields.List(fields.Int)
    owners = fields.List(fields.Int)
    subscribers = fields.List(fields.Int, allow_none=True)
    created = fields.DateTime(allow_none=True)
    updated = fields.DateTime(allow_none=True)

    @post_load
    def make_user(self, data, **kwargs):
        return ShoppingList(**data)
