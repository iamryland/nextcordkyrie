# __init__.py - code by Rye
import sqlite3

from ._guild import Guild as cGuild
import warehouse.database.access as dba

with open('../database/discordmaster.sql') as f:
    data = f.read()

con: sqlite3.Connection
con = dba.connect('master', 'init')
con.executescript(data)
con.commit()
dba.disconnect('init')
