# _sector.py - code by Rye
import warehouse.database.access as dba


class ValueHolder:
    def __init__(self, value, key, doc):
        self.value = value
        self.key = key
        self.doc = doc


class Sector:
    def __init__(self, gid, table):
        self._dba = dba
        self.gid = gid
        self._table = table
        self.key = table
        self.values = {}

    def _update_db(self, opt, data):
        """Updates a single field in a database record"""
        con = self._dba.connect('master', 'master')
        con.execute(f"UPDATE {self._table} SET {opt}=:data WHERE id={self.gid}", {'data': data})
        con.commit()

    def _retrieve_db(self, opt):
        """Retrieves data from a single field in a database record"""
        con = self._dba.connect('master', 'master')
        cur = con.execute(f"SELECT {opt} FROM {self._table} WHERE id={self.gid}")
        result = cur.fetchone()
        con.commit()
        if result:
            return result[0]
        else:
            return None

    def _new_record(self):
        """Creates a new database record"""
        con = self._dba.connect('master', 'master')
        con.execute(f"INSERT INTO {self._table} (id, stat) VALUES (:id, :stat)", {'id': self.gid, 'stat': 1})
        con.commit()

    def _check_db(self):
        """Checks the database for an existing record"""
        result = self._retrieve_db('id')
        if result:
            return False
        else:
            return True

    @property
    def stat(self) -> int:
        return self._retrieve_db('stat')

    @stat.setter
    def stat(self, stat: int):
        self._update_db('stat', stat)
