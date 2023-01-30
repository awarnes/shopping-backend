from .users import get_users


ROUTES = {
    '/users': {'view_func': get_users, 'methods': ['GET']}
}