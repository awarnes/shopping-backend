from flask import jsonify, request

from ..handlers import users

def get_users():
    gottenUsers = users.get_users()
    print(gottenUsers)
    return jsonify(gottenUsers)