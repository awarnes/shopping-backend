from dataclasses import dataclass
from typing import List, Optional
from marshmallow import Schema, fields, post_load

class ShoppingList:
    def __init__(
        self,
        items: List[int],
        owners: List[int],
        subscribers: Optional[List[int]],
        id: Optional[int] = None,
        created: Optional[str] = None,
        updated: Optional[str] = None
    ):
        self.id = id
        self.items = items
        self.owners = owners
        self.subscribers = subscribers
        self.created = created
        self.updated = updated

class ShoppingListSchema(Schema):
    id = fields.Int(allow_none=True)
    items = fields.List(fields.Int)
    owners = fields.List(fields.Int)
    subscribers = fields.List(fields.Int, allow_none=True)
    created = fields.DateTime(allow_none=True)
    updated = fields.DateTime(allow_none=True)

    @post_load
    def make_user(self, data, **kwargs):
        return ShoppingList(**data)
