# access.py - code by Rye

# This file contains the code/methods to access the various databases.
# These are mostly connections and cursors, but there is some logic built in.
import sqlite3 as sql
import os

BASE_PATH = 'warehouse/database'
databases = {}


def connect(database: str, user: str, con='db'):
    if user in databases.keys():
        return databases[user][con]
    else:
        new_con = sql.connect(f'{BASE_PATH}/{database}.db')
        new_cursor = new_con.cursor()
        databases[user] = {"db": new_con, "cursor": new_cursor}
        return databases[user][con]


def disconnect(user: str):
    if user in databases.keys():
        databases[user]['db'].close()
    else:
        pass


def cleanup():
    for k, v in databases.items():
        v['db'].close()
        print(f'Deleting access point [{k}] ...')
    os.system('cls')
