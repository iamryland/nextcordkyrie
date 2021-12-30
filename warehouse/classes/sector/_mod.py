# _mod.py - code by Rye
from _sector import Sector


class Mod(Sector):
    def __init__(self, gid: int):
        super().__init__(gid, 'mod')
        if self.check_db():
            self.new_record()
            self.reports = None
            self.mods = None
        self._stat = self.retrieve_db('stat')
        self._reports = self.retrieve_db('reports')
        self._mods = self.retrieve_db('mods')

    def __str__(self):
        return 'Mod Features'

    def __repr__(self):
        return f'Mod Features - gID: {self.gid}'

    @property
    def stat(self):
        return self._stat

    @stat.setter
    def stat(self, stat):
        self._stat = stat
        self.update_db('stat', stat)

    @property
    def reports(self):
        return self._reports

    @reports.setter
    def reports(self, data):
        self._reports = data
        self.update_db('reports', data)

    @property
    def mods(self):
        return self._mods

    @mods.setter
    def mods(self, data):
        self._mods = data
        self.update_db('mods', data)
