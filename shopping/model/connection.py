import sqlite3
import os
from contextlib import closing

DATABASE_NAME = 'shopping.db'
DB_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../db')

def get_connection():
    return sqlite3.connect(os.path.join(DB_DIRECTORY, DATABASE_NAME))

def fetch_one(sql, data=[]):
    with closing(get_connection()) as conn:
        with conn:
            conn.row_factory = sqlite3.Row
            with closing(conn.cursor()) as cur:
                cur.execute(sql, data)
                return cur.fetchone()

def fetch_all(sql, data=[]):
    with closing(get_connection()) as conn:
        with conn:
            conn.row_factory = sqlite3.Row
            with closing(conn.cursor()) as cur:
                cur.execute(sql, data)
                return cur.fetchall()

def insert_one(sql, data=[]):
    with closing(get_connection()) as conn, conn, \
        closing(conn.cursor()) as cur:
            cur.execute(sql, data)

def insert_many(sql, data=[]):
    with closing(get_connection()) as conn, conn, \
        closing(conn.cursor()) as cur:
            cur.executemany(sql, data)