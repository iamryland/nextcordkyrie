# _mod.py - code by Rye
import json
from ._sector import Sector, ValueHolder


class Mod(Sector):
    """Allows the bot to run moderation commands"""
    def __init__(self, gid: int):
        super().__init__(gid, 'mod')
        if self._check_db():
            self._new_record()
            self.reports = None
            self.mods = None
            self.stat = self._retrieve_db('stat')
        with open('warehouse/database/json/mod.json') as file:
            data = json.load(file)
            for k, v in data.items():
                self.values[k] = ValueHolder(self._retrieve_db(k), k, v)

    def __str__(self):
        return 'Mod Features'

    def __repr__(self):
        return f'Mod Features - gID: {self.gid}'

    @property
    def reports(self):
        value = self._retrieve_db('reports')
        self.values['reports'].value = value
        return value

    @reports.setter
    def reports(self, data):
        self.values['reports'].value = data
        self._update_db('reports', data)

    @property
    def mods(self):
        value = self._retrieve_db('mods')
        self.values['mods'].value = value
        return value

    @mods.setter
    def mods(self, data):
        self.values['mods'].value = data
        self._update_db('mods', data)
