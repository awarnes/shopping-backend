import sqlite3
import os

DATABASE_NAME = 'shopping.db'
DB_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
BASE_SQL_FILE = os.path.join(DB_DIRECTORY, 'base.sql')
PATCHES_DIRECTORY = os.path.join(DB_DIRECTORY, 'patches')
EXCLUSION_LIST = ['.gitkeep']

def get_connection():
    return sqlite3.connect(os.path.join(DB_DIRECTORY, DATABASE_NAME))

def get_patches():
    '''Get all patch files and data from patches directory'''
    patches = {}
    filenames = next(os.walk(PATCHES_DIRECTORY), (None, None, []))[2]

    for file in filenames:
        with open(os.path.join(PATCHES_DIRECTORY, file)) as f:
            patches[file] = f.read()

    return patches

def check_patch_history(filename):
    '''Check the patch history table for a given patch name'''

    connection = get_connection()

    with connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM patch_history WHERE patch_name = :patch_name", {"patch_name": filename})

        return cursor.fetchone()


def set_up_db():
    '''Create db if it doesn't exist and create base table if it doesn't exist'''

    connection = get_connection()

    with connection:
        cursor = connection.cursor()
        with open(os.path.join(DB_DIRECTORY, 'base.sql')) as f:
            cursor.executescript(f.read())

def apply_patches():
    '''Apply any patches that haven't been applied to the database'''

    patches = get_patches()

    connection = get_connection()
    cursor = connection.cursor()

    with connection:
        for patch_name, patch in patches.items():
            print(f"XKCD: {check_patch_history(patch_name)}")
            if not check_patch_history(patch_name) and patch_name not in EXCLUSION_LIST:
                cursor.executescript(patch)

                cursor.execute('''
                    INSERT INTO patch_history (patch_name)
                    VALUES (:patch_name);
                    ''',
                    {'patch_name': patch_name}
                )

                print(f"Applied patch {patch_name} to {DATABASE_NAME}")
            else:
                if patch_name in EXCLUSION_LIST:
                    print(f"Skipping: {patch_name} for {DATABASE_NAME} in the exclusion list")
                else:
                    print(f"Skipping: {patch_name} already applied to {DATABASE_NAME}")


def test():
    connection = get_connection()
    with connection:
        cursor = connection.cursor()
        cursor.execute('select * from sqlite_master')
        return cursor.fetchall()