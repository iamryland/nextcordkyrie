# _modone.py - code by Rye
from ._sector import Sector


class ModOne(Sector):
    """The Advanced Auto-Mod features"""
    def __init__(self, gid: int):
        super().__init__(gid, 'modone')
        if self._check_db():
            self._new_record()
            self.stat = self._retrieve_db('stat')
        self._json = self._retrieve_db('json')
        self._filters = self._retrieve_db('filters')
        self.docs = {'json': 'Various auto-moderation data', 'filters': 'The status of the chat filters'}

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
        self._update_db('json', data)

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, data):
        self._filters = data
        self._update_db('filters', data)
