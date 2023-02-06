from enum import Enum
from flask import g
from ..handlers.shopping_lists import get_list_by_id

class Roles(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    ANONYMOUS = "ANONYMOUS"

class Permission(str, Enum):
    ALL = "ALL"
    CREATE_USER = "CREATE_USER"
    READ_SELF_USER = "READ_SELF_USER"
    UPDATE_SELF_USER = "UPDATE_SELF_USER"
    DELETE_SELF_USER = "DELETE_SELF_USER"
    READ_ANY_USER = "READ_ANY_USER"
    UPDATE_ANY_USER = "UPDATE_ANY_USER"
    DELETE_ANY_USER = "DELETE_ANY_USER"
    CREATE_SELF_LIST = "CREATE_SELF_LIST"
    READ_SELF_LIST = "READ_SELF_LIST"
    UPDATE_SELF_LIST = "UPDATE_SELF_LIST"
    DELETE_SELF_LIST = "DELETE_SELF_LIST"
    CREATE_ANY_LIST = "CREATE_ANY_LIST"
    READ_ANY_LIST = "READ_ANY_LIST"
    UPDATE_ANY_LIST = "UPDATE_ANY_LIST"
    DELETE_ANY_LIST = "DELETE_ANY_LIST"
    CREATE_SELF_PRODUCT = "CREATE_SELF_PRODUCT"
    READ_SELF_PRODUCT = "READ_SELF_PRODUCT"
    UPDATE_SELF_PRODUCT = "UPDATE_SELF_PRODUCT"
    DELETE_SELF_PRODUCT = "DELETE_SELF_PRODUCT"
    CREATE_ANY_PRODUCT = "CREATE_ANY_PRODUCT"
    READ_ANY_PRODUCT = "READ_ANY_PRODUCT"
    UPDATE_ANY_PRODUCT = "UPDATE_ANY_PRODUCT"
    DELETE_ANY_PRODUCT = "DELETE_ANY_PRODUCT"

ROLE_MAP = {
    Roles.ADMIN: [Permission.ALL],
    Roles.USER: [
        Permission.READ_SELF_USER,
        Permission.UPDATE_SELF_USER,
        Permission.DELETE_SELF_USER,
        Permission.READ_ANY_USER,
        Permission.CREATE_SELF_LIST,
        Permission.READ_SELF_LIST,
        Permission.UPDATE_SELF_LIST,
        Permission.DELETE_SELF_LIST,
        Permission.READ_ANY_LIST,
        Permission.CREATE_SELF_PRODUCT,
        Permission.READ_SELF_PRODUCT,
        Permission.UPDATE_SELF_PRODUCT,
        Permission.DELETE_SELF_PRODUCT,
        Permission.READ_ANY_PRODUCT
    ],
    Roles.ANONYMOUS: [
        Permission.CREATE_USER,
        Permission.READ_ANY_LIST,
        Permission.READ_ANY_PRODUCT
    ]
}

class PermissionException(Exception):
    pass

def validate_self_permission(data) -> bool:
    return g.current_user.id == data["user_id"]

def validate_ownership_permission(data) -> bool:
    if list_id := data.get('list_id'):
        return g.current_user.id in get_list_by_id(list_id).owners

PERMISSIONS_MAP = {
    Permission.CREATE_SELF_LIST: validate_self_permission,
    Permission.UPDATE_SELF_LIST: validate_ownership_permission
}

def verify_permission(perm: Permission, *args, **kwargs):
    validate_func = PERMISSIONS_MAP.get(perm)

    if not validate_func:
        return True
    
    return validate_func({"args": args, **kwargs})