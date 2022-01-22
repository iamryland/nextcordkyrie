# _levels.py - code by Rye
import sqlite3
from os import path
import warehouse.database.access as dba
from ._sector import Sector


class Levels(Sector):
    """The leveling system, which ranks users based on activity."""
    def __init__(self, gid: int):
        self.con: sqlite3.Connection
        super().__init__(gid, 'levels')
        self._ldb = dba.connect(f'guilds/{gid}', f'Levels-{self.gid}')
        with open('warehouse/database/levels.sql') as file:
            data = file.read()
        self._ldb.executescript(data)
        self._ldb.commit()
        if self._check_db():
            self._new_record()
            self.stat = self._retrieve_db('stat')
        self.docs = {'type': 'The type of leveling system used',
                     'multi': 'The multiplier for the server',
                     'roles': 'Level-specific roles',
                     'custom': 'Any custom data saved',
                     'exclude': 'Channels that do not gain XP'
                     }

    def __str__(self):
        return 'Levels'

    def __repr__(self):
        return f'Levels - gID: {self.gid}'

    @property
    def type(self):
        return self._retrieve_db('type')

    @type.setter
    def type(self, data):
        self._update_db('type', data)

    @property
    def multi(self):
        return self._retrieve_db('multi')

    @multi.setter
    def multi(self, data):
        self._update_db('multi', data)

    @property
    def roles(self):
        return self._retrieve_db('roles')

    @roles.setter
    def roles(self, data):
        self._update_db('roles', data)

    @property
    def custom(self):
        return self._retrieve_db('custom')

    @custom.setter
    def custom(self, data):
        self._update_db('custom', data)

    @property
    def exclude(self):
        return self._retrieve_db('exclude')

    @exclude.setter
    def exclude(self, data):
        self._update_db('exclude', data)
