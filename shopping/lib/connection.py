import sqlite3
import os
from contextlib import closing

DATABASE_NAME = 'shopping.db'
DB_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../db')

def get_connection():
    return sqlite3.connect(os.path.join(DB_DIRECTORY, DATABASE_NAME))

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def fetch_one(sql, params=[]):
    with closing(get_connection()) as conn:
        with conn:
            conn.row_factory = dict_factory
            with closing(conn.cursor()) as cur:
                cur.execute(sql, params)
                return cur.fetchone()

def fetch_all(sql, params=[]):
    with closing(get_connection()) as conn:
        with conn:
            conn.row_factory = dict_factory
            with closing(conn.cursor()) as cur:
                cur.execute(sql, params)
                return cur.fetchall()

def insert_one(sql, params=[]):
    with closing(get_connection()) as conn, conn, \
        closing(conn.cursor()) as cur:
            cur.execute(sql, params)
            return True

def insert_many(sql, params=[]):
    with closing(get_connection()) as conn, conn, \
        closing(conn.cursor()) as cur:
            cur.executemany(sql, params)
            return True