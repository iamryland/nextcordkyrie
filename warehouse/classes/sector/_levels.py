# _levels.py - code by Rye
import sqlite3
import json
import warehouse.database.access as dba
from ._sector import Sector, ValueHolder


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
        with open('warehouse/database/json/levels.json') as file:
            data = json.load(file)
            for k, v in data.items():
                self.values[k] = ValueHolder(self._retrieve_db(k), k, v)

    def __str__(self):
        return 'Levels'

    def __repr__(self):
        return f'Levels - gID: {self.gid}'

    @property
    def type(self):
        value = self._retrieve_db('type')
        self.values['type'].value = value
        return value

    @type.setter
    def type(self, data):
        self.values['type'].value = data
        self._update_db('type', data)

    @property
    def multi(self):
        value = self._retrieve_db('multi')
        self.values['multi'].value = value
        return value

    @multi.setter
    def multi(self, data):
        self.values['multi'].value = data
        self._update_db('multi', data)

    @property
    def roles(self):
        value = self._retrieve_db('roles')
        self.values['roles'].value = value
        return value

    @roles.setter
    def roles(self, data):
        self.values['roles'].value = data
        self._update_db('roles', data)

    @property
    def custom(self):
        value = self._retrieve_db('custom')
        self.values['custom'].value = value
        return value

    @custom.setter
    def custom(self, data):
        self.values['custom'].value = data
        self._update_db('custom', data)

    @property
    def exclude(self):
        value = self._retrieve_db('exclude')
        self.values['exclude'].value = value
        return value

    @exclude.setter
    def exclude(self, data):
        self.values['exclude'].value = data
        self._update_db('exclude', data)
