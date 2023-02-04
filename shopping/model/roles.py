from enum import Enum
from flask import g

class Roles(str, Enum):
    ADMIN = "admin"
    USER = "user"
    ANONYMOUS = "anonymous"

class Permission(str, Enum):
    ALL = "all"
    CREATE_USER = "create_user"
    READ_SELF_USER = "read_self_user"
    UPDATE_SELF_USER = "update_self_user"
    DELETE_SELF_USER = "delete_self_user"
    READ_ANY_USER = "read_any_user"
    UPDATE_ANY_USER = "update_any_user"
    DELETE_ANY_USER = "delete_any_user"
    CREATE_SELF_LIST = "create_self_list"
    READ_SELF_LIST = "read_self_list"
    UPDATE_SELF_LIST = "update_self_list"
    DELETE_SELF_LIST = "delete_self_list"
    CREATE_ANY_LIST = "create_any_list"
    READ_ANY_LIST = "read_any_list"
    UPDATE_ANY_LIST = "update_any_list"
    DELETE_ANY_LIST = "delete_any_list"
    CREATE_SELF_PRODUCT = "create_self_product"
    READ_SELF_PRODUCT = "read_self_product"
    UPDATE_SELF_PRODUCT = "update_self_product"
    DELETE_SELF_PRODUCT = "delete_self_product"
    CREATE_ANY_PRODUCT = "create_any_product"
    READ_ANY_PRODUCT = "read_any_product"
    UPDATE_ANY_PRODUCT = "update_any_product"
    DELETE_ANY_PRODUCT = "delete_any_product"

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

PERMISSIONS_MAP = {
    Permission.CREATE_SELF_LIST: validate_self_permission
}

def verify_permission(perm: Permission, *args, **kwargs):
    validate_func = PERMISSIONS_MAP[perm]

    if not validate_func:
        return True
    
    return validate_func({"args": args, **kwargs})