# _guild.py - code by Rye
import warehouse.database.access
from . import sector
import json


_SECTORS = ('Mod', 'ModOne', 'Levels')


class Guild:
    def __init__(self, gid: int, name: str, db: warehouse.database.access, announce=None, check=True):
        self.dba = db
        self.gid = gid
        self._name = name
        self.__check = check
        self._announce = None
        if self.check_db():
            self.new_record()
        else:
            self.update_db('name', self.name)
        if announce:
            self.announce = announce
        else:
            self._announce: int = self.retrieve_db('announce')
        with open('warehouse/database/master.json', 'r') as file:
            data = json.load(file)
            if self.gid in data.keys():
                prefix = data[f'{self.gid}']
            else:
                prefix = '.'
                data[f'{self.gid}'] = prefix
        with open('warehouse/database/master.json', 'w') as file:
            json.dump(data, file)
        self._prefix = prefix
        self._cmds: str = self.retrieve_db('cmds')
        self.sectors = []
        for value in _SECTORS:
            self.sectors.append(getattr(sector, value)(self.gid))

    def update_db(self, opt, data):
        """Updates a field in the database"""
        con = self.dba.connect('master', 'Guild')
        con.execute(f"UPDATE config SET {opt}=:data WHERE id={self.gid}", {'data': data})
        con.commit()

    def retrieve_db(self, opt):
        """Retrieves data from a single field in a database record"""
        con = self.dba.connect('master', 'Guild')
        cur = self.dba.connect('master', 'Guild', 'cursor')
        cur.execute(f"SELECT {opt} FROM config WHERE id={self.gid}")
        result = cur.fetchone()
        con.commit()
        if result:
            return result[0]
        else:
            return None

    def check_db(self):
        """Checks the database for an existing record"""
        result = self.retrieve_db('id')
        if result:
            return False
        else:
            return True

    def new_record(self):
        """Creates a new database record"""
        con = self.dba.connect('master', 'Guild')
        con.execute("INSERT INTO config (id, name) VALUES (:id, :name)", {'id': self.gid, 'name': self.name})

    def get_feat(self):
        to_send = f'```Guild features for [ {self.name} ]:<{self.gid}>:\n'
        for value in self.sectors:
            if value.stat == 0:
                to_send += f'   |>- {value}\n'
        to_send += '```'
        return to_send

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
        self.update_db('name', name)

    @property
    def prefix(self) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self, prefix: str):
        self._prefix = prefix
        with open('warehouse/database/master.json', 'r') as file:
            data = json.load(file)
            data[f'{self.gid}'] = self._prefix
            json.dump(data, file)

    @property
    def announce(self) -> int:
        return self._announce

    @announce.setter
    def announce(self, announce: int):
        self._announce = announce
        self.update_db('announce', announce)

    @property
    def cmds(self) -> str:
        return self._cmds

    @cmds.setter
    def cmds(self, cmds: str):
        self._cmds = cmds
        self.update_db('cmds', cmds)
