# _mod.py - code by Rye
from ._sector import Sector


class Mod(Sector):
    """Allows the bot to run moderation commands"""
    def __init__(self, gid: int):
        super().__init__(gid, 'mod')
        if self._check_db():
            self._new_record()
            self.reports = None
            self.mods = None
            self.stat = self._retrieve_db('stat')
        self._reports = self._retrieve_db('reports')
        self._mods = self._retrieve_db('mods')
        self.docs = {'reports': 'The reports channel for mod events', 'mods': 'The roles allowed to use moderation commands'}

    def __str__(self):
        return 'Mod Features'

    def __repr__(self):
        return f'Mod Features - gID: {self.gid}'

    @property
    def reports(self):
        return self._reports

    @reports.setter
    def reports(self, data):
        self._reports = data
        self._update_db('reports', data)

    @property
    def mods(self):
        return self._mods

    @mods.setter
    def mods(self, data):
        self._mods = data
        self._update_db('mods', data)
