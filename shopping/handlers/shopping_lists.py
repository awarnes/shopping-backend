import json
from typing import List
from marshmallow import ValidationError
from ..lib.connection import fetch_all, fetch_one, insert_one
from ..model.product import Product
from ..model.shopping_list import ShoppingList, ShoppingListSchema

def get_lists_for_user(id: int) -> ShoppingList | List:
    try:
        rows = fetch_all("SELECT * FROM lists;")
        filtered_rows = filter(lambda row: id in row['owners'], rows)
        return ShoppingListSchema().load(filtered_rows, many=True)
    except ValidationError as error:
        print(f"Error getting lists {error}")
        return False

def get_list_by_id(id: int) -> ShoppingList | dict:
    shopping_list = fetch_one("SELECT * FROM lists WHERE id = :id;", {"id": id})
    if shopping_list:
        return ShoppingListSchema().load(shopping_list)
    return False

def create_list_for_user(user_id: int, shopping_list: ShoppingList) -> bool:
    owners = set(shopping_list.owners)
    owners.add(user_id)
    return insert_one(
        "INSERT INTO lists (products, owners, subscribers, name) VALUES (:products, :owners, :subscriber, :name);",
        {
            "name": shopping_list.name,
            "products": str(shopping_list.products),
            "owners": str(list(owners)),
            "subscribers": str(shopping_list.subscribers)
        }
    )

def update_list(shopping_list: ShoppingList):
    return insert_one(
        '''
        INSERT INTO lists (id, products, owners, subscribers, name)
        VALUES (:id, :products, :owners, :subscriber, :name)
        ON CONFLICT (id) DO UPDATE SET
            name = excluded.name,
            products = excluded.products,
            owners = excluded.owners,
            subscribers = excluded.subscribers;
        ''',
        {
            "id": shopping_list.id,
            "name": shopping_list.name,
            "products": json.dump(shopping_list.products),
            "owners": json.dump(),
            "subscribers": json.dump(shopping_list.subscribers)
        }
    )

def add_products_to_list(list_id: int, products: List[Product]) -> ShoppingList:
    shopping_list = get_list_by_id(list_id)
    if shopping_list:
        shopping_list.products += [product.id for product in products]
        if update_list(shopping_list):
            return shopping_list

def add_subscribers_to_list(list_id: int, subscribers: List[int]) -> ShoppingList:
    shopping_list = get_list_by_id(list_id)
    if shopping_list:
        shopping_list.subscribers += subscribers
        if update_list(shopping_list):
            return shopping_list

def add_owners_to_list(list_id: int, owners: List[int]) -> ShoppingList:
    shopping_list = get_list_by_id(list_id)
    if shopping_list:
        shopping_list.subscribers += owners
        if update_list(shopping_list):
            return shopping_list