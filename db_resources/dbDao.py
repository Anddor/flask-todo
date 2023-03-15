import contextlib
import sqlite3

DATABASE_FILE = 'database.db'


class DbDAO(object):
    def __init__(self):
        self.setup_database()
        pass

    def _execute_sql(self, statement, values):
        """Kjører SQL-spørringen 'statement' med gitte verdi-bindinger 'values' og returnerer"""
        with contextlib.closing(sqlite3.connect(DATABASE_FILE)) as conn:  # auto-closes
            with conn:  # auto-commits
                conn.row_factory = sqlite3.Row  # wrap for named columns
                with contextlib.closing(conn.cursor()) as cursor:  # auto-closes
                    cursor.execute(statement, values)
                    fetch = cursor.fetchall()
                    lastrow = cursor.lastrowid
                    return fetch, lastrow

    def _execute_sql_fetchall(self, statement, values):
        """Kjører SQL-spørringen og returnerer verdiene. Bruk til SELECT og RETURNING."""
        fetch, _ = self._execute_sql(statement, values)
        return fetch

    def _execute_sql_lastrowid(self, statement, values):
        """Kjører SQL-spørringen og returnerer iden til siste rad. Bruk til INSERT."""
        _, lastrow = self._execute_sql(statement, values)
        return lastrow

    def _map_all_rows(self, rows):
        """Mapper alle rader til dict og returnerer en liste med dicts."""
        return [dict(row) for row in rows]

    def _map_single_row(self, row):
        """Mapper en rad til dict. Kaster exception hvis det er mer enn en rad"""
        r = self._map_all_rows(row)
        if len(r) > 1:
            raise Exception('Expected one row, got ' + str(len(r)))
        return r[0]

    def get(self, id):
        """EKSEMPEL: Henter en rad fra todo tabellen basert på id"""
        todo = self._execute_sql_fetchall('''SELECT id, task, fav FROM todo WHERE id = :id''',
                                          {'id': id})
        return self._map_single_row(todo)

    # ---- OPPGAVER ----

    def setup_database(self):
        # OPPGAVE: Skriv SQL som oppretter tabellen todo
        try:
            self._execute_sql(
                '''
                SQL HER
                ''', {})
        except:
            pass

    def get_all(self):
        # OPPGAVE: Skriv SQL som henter alle rader fra todo tabellen

        todos = self._execute_sql_fetchall(
            '''
            SQL HER
            ''', {})
        return self._map_all_rows(todos)

    def insert(self, data):
        # OPPGAVE: Skriv SQL som setter inn en ny rad i todo tabellen
        inserted = self._execute_sql_fetchall(
            '''
            SQL HER
            ''', data)
        return self._map_single_row(inserted)

    def update(self, id, data):
        # OPPGAVE: Skriv SQL som oppdaterer den gitte raden i tabellen
        values = dict()  # OPPGAVE: Fyll inn verdier
        self._execute_sql(
            '''
            SQL HER
            ''', values)
        return data

    def delete(self, id):
        # OPPGAVE: Skriv SQL som sletter den gitte raden i tabellen
        self._execute_sql(
            '''
            SQL HER
            ''', {})
