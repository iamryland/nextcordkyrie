# _modone.py - code by Rye
import json
from ._sector import Sector, ValueHolder


class ModOne(Sector):
    """The Advanced Auto-Mod features"""
    def __init__(self, gid: int):
        super().__init__(gid, 'modone')
        if self._check_db():
            self._new_record()
            self.stat = self._retrieve_db('stat')
        with open('warehouse/database/json/modone.json') as file:
            data = json.load(file)
            for k, v in data.items():
                self.values[k] = ValueHolder(self._retrieve_db(k), k, v)

    def __str__(self):
        return 'ModOne'

    def __repr__(self):
        return f'ModOne-{self.gid}'

    @property
    def json(self):
        value = self._retrieve_db('json')
        self.values['json'].value = value
        return value

    @json.setter
    def json(self, data):
        self.values['json'].value = data
        self._update_db('json', data)

    @property
    def filters(self):
        value = self._retrieve_db('filters')
        self.values['filters'].value = value
        return value

    @filters.setter
    def filters(self, data):
        self.values['filters'].value = data
        self._update_db('filters', data)
