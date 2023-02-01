from flask import g
from marshmallow import ValidationError
from ..lib.connection import fetch_all, fetch_one, insert_one
from ..model.shopping_list import ShoppingList, ShoppingListSchema

def get_lists_for_user(id: int) -> ShoppingList | ValidationError:
    try:
        rows = fetch_all(
            "SELECT * FROM lists WHERE owners LIKE '%:user_id,%'",
            {"user_id": id}
        )
        return ShoppingListSchema().load(rows, many=True)
    except ValidationError as error:
        print(f"Error getting lists {error}")
        return []

def get_list_by_id(id: int) -> ShoppingList | dict:
    shopping_list = fetch_one("SELECT * FROM lists WHERE id = :id;", {"id": id})
    if shopping_list:
        return ShoppingListSchema().load(shopping_list)
    return {}

def create_list_for_user(user_id: int, list: ShoppingList):
    owners = set(list.owners)
    owners.add(user_id)
    return insert_one(
        "INSERT INTO lists (items, owners, subscribers) VALUES (:items, :owners, :subscribers);",
        {"items": str(list.items), "owners": str(list(owners)), "subscribers": str[list.subscribers]}
    )