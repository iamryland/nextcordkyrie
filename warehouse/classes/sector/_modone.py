# _modone.py - code by Rye
from ._sector import Sector


class ModOne(Sector):
    def __init__(self, gid: int):
        super().__init__(gid, 'modone')
        if self.check_db():
            self.new_record()
        self._json = self.retrieve_db('json')
        self._filters = self.retrieve_db('filters')

    def __str__(self):
        return 'ModOne'

    def __repr__(self):
        return f'ModOne-{self.gid}'

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, data):
        self._json = data
        self.update_db('json', data)

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, data):
        self._filters = data
        self.update_db('filters', data)
