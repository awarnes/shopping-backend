from dataclasses import dataclass, field
from typing import List, Optional
from marshmallow import Schema, fields, post_load
from .preferences import Brand

@dataclass
class Location:
    # Directly from Kroger API
    bay_number: Optional[str] = None
    description: Optional[str] = None
    number: Optional[str] = None
    number_of_facings: Optional[str] = None
    shelf_number: Optional[str] = None
    shelf_position_in_bay: Optional[str] = None
    side: Optional[str] = None

class LocationSchema(Schema):
    bay_number = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    number = fields.Str(allow_none=True)
    number_of_facings = fields.Str(allow_none=True)
    shelf_number = fields.Str(allow_none=True)
    shelf_position_in_bay = fields.Str(allow_none=True)
    side = fields.Str(allow_none=True)

    @post_load
    def make_location(self, data, **kwargs):
        return Location(**data)

@dataclass
class Product:
    name: str
    brand: Brand
    sku: str
    location: Optional[Location] = None
    id: Optional[int] = None
    tags: Optional[List[str]] = field(default_factory=[])
    created: Optional[str] = None
    updated: Optional[str] = None

class ProductSchema(Schema):
    name = fields.Str()
    brand = fields.Enum(enum=Brand)
    sku = fields.Str()
    location = fields.Nested(LocationSchema(), allow_none=True)
    id = fields.Int(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    created = fields.Str(allow_none=True)
    updated = fields.Str(allow_none=True)

    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)
