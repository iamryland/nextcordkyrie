# _levels.py - code by Rye
import sqlite3
from os import path
import warehouse.database.access as dba
from _sector import Sector


class Levels(Sector):
    def __init__(self, gid: int):
        self.con: sqlite3.Connection
        self.ldb = dba.connect(f'guilds/{gid}', __name__)
        super().__init__(gid, 'levels')
        if self.check_db():
            self.new_record()
        self._stat = self.retrieve_db('stat')
        self._multi = self.retrieve_db('multi')
        self._type = self.retrieve_db('type')
        self._roles = self.retrieve_db('roles')
        self._custom = self.retrieve_db('custom')
        self._exclude = self.retrieve_db('exclude')

        if path.isfile(f'../../database/guilds/{gid}.db'):
            pass
        else:
            with open('../../database/levels.sql') as file:
                data = file.read()
            self.ldb.executescript(data)
            self.ldb.commit()

    def __str__(self):
        return 'Levels'

    def __repr__(self):
        return f'Levels - gID: {self.gid}'

    @property
    def ltype(self):
        return self._type

    @ltype.setter
    def ltype(self, data):
        self._type = data
        self.update_db('type', data)

    @property
    def multi(self):
        return self._multi

    @multi.setter
    def multi(self, data):
        self._multi = data
        self.update_db('multi', data)

    @property
    def roles(self):
        return self._roles

    @roles.setter
    def roles(self, data):
        self._roles = data
        self.update_db('roles', data)

    @property
    def custom(self):
        return self._custom

    @custom.setter
    def custom(self, data):
        self._custom = data
        self.update_db('custom', data)

    @property
    def exclude(self):
        return self._exclude

    @exclude.setter
    def exclude(self, data):
        self._exclude = data
        self.update_db('exclude', data)

    @property
    def stat(self):
        return self._stat

    @stat.setter
    def stat(self, stat):
        self._stat = stat
        self.update_db('stat', stat)
