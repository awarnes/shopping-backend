import sqlite3
import os

DATABASE_NAME = 'shopping.db'
DB_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../db')

def get_connection():
    return sqlite3.connect(os.path.join(DB_DIRECTORY, DATABASE_NAME))