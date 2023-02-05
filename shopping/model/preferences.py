from enum import Enum
from marshmallow import Schema, fields, post_load
from .brand import Brand

class BrandPreferences(object):
    def __init__(self, preferred_store, brand):
        self.brand = brand
        self.preferred_store = preferred_store

class BrandPreferencesSchema(Schema):
    brand = fields.Enum(enum=Brand)
    preferred_store = fields.Str(allow_none=True)

class KrogerPreferences(BrandPreferences):
    def __init__(self, preferred_store):
        super(KrogerPreferences, self).__init__(preferred_store, Brand.KROGER)

class KrogerPreferencesSchema(BrandPreferencesSchema):
    @post_load
    def make_kroger_preferences(self, data, **kwargs):
        return KrogerPreferences(**data)

class TraderJoesPreferences(BrandPreferences):
    def __init__(self, preferred_store):
        super(TraderJoesPreferences, self).__init__(preferred_store, Brand.KROGER)  

class TraderJoesPreferencesSchema(BrandPreferencesSchema):
    @post_load
    def make_trader_joes_preferences(self, data, **kwargs):
        return TraderJoesPreferences(**data)

class UserPreferences:
    def __init__(self, preferred_brand: Brand):
        self.preferred_brand = preferred_brand

class UserPreferencesSchema(Schema):
    brand = fields.Enum(enum=Brand)

    @post_load
    def make_user_preferences(self, data, **kwargs):
        return UserPreferences(**data)

class Preferences:
    def __init__(
        self,
        kroger: KrogerPreferences,
        trader_joes: TraderJoesPreferences,
        user: UserPreferences
    ):
        self.kroger = KrogerPreferences(kroger)
        self.trader_joes = TraderJoesPreferences(trader_joes)
        self.user = UserPreferences(user)

class PreferencesSchema(Schema):
    kroger = fields.Nested(KrogerPreferencesSchema)
    trader_joes = fields.Nested(TraderJoesPreferencesSchema)
    user = fields.Nested(UserPreferencesSchema)

    @post_load
    def make_preferences(self, data, **kwargs):
        return Preferences(**data)
