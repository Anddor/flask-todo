import contextlib
import os
import sqlite3

from daoInterface import DaoInterface

DATABASE_FILE = 'database.db'


class DbDAO(DaoInterface):
    def __init__(self):
        self.setup_database()
        pass

    """
    Kjører SQL-spørringen 'statement' med gitte verdi-bindinger 'values'
    """

    def _execute_sql(self, statement, values):
        with contextlib.closing(sqlite3.connect(DATABASE_FILE)) as conn:  # auto-closes
            with conn:  # auto-commits
                conn.row_factory = sqlite3.Row  # wrap for named columns
                with contextlib.closing(conn.cursor()) as cursor:  # auto-closes
                    cursor.execute(statement, values)
                    fetch = cursor.fetchall()
                    lastrow = cursor.lastrowid
                    return fetch, lastrow

    """
    Kjører SQL-spørringen om returnere alt som matcher, bruk til SELECT.
    """

    def _execute_sql_fetchall(self, statement, values):
        fetch, _ = self._execute_sql(statement, values)
        return fetch

    """
    Kjører SQL-spørringen og returnerer iden til siste rad. Bruk til INSERT.
    """

    def _execute_sql_lastrowid(self, statement, values):
        _, lastrow = self._execute_sql(statement, values)
        return lastrow

    def _map_row(self, row):
        return dict(row)

    def _map_rows(self, rows):
        return [dict(row) for row in rows]
    """
    Opprett tabeller i databasen om database-filen ikke finnes fra før.
    """

    def setup_database(self):
        try:
            self._execute_sql('''CREATE TABLE todo (id INTEGER PRIMARY KEY, task TEXT, fav INTEGER)
            ''', {})
        except:
            pass

    def get_all(self):
        # fetch all todos from database

        todos = self._execute_sql_fetchall(
            '''SELECT id, task, fav FROM todo''', {})
        return self._map_rows(todos)

    def get(self, id):

        # fetch the todo with the given id
        todo = self._execute_sql('''SELECT id, task, fav FROM todo WHERE id = :id''',
                                 {'id': id})
        return self._map_row(todo)

    def insert(self, data):
        todo = data
        # OPPGAVE: Skriv SQL som setter inn en ny rad i todo tabellen
        todo_id = self._execute_sql_lastrowid('''
        INSERT INTO todo (task, fav) VALUES (:task, :fav)
        ''', data)

        todo['id'] = todo_id
        return todo

    def update(self, id, data):
        # OPPGAVE: Skriv SQL som oppdaterer den gitte raden i tabellen
        data['id'] = id
        self._execute_sql('''
        UPDATE todo SET task = :task, fav = :fav WHERE id = :id
        ''', data)
        return data

    def delete(self, id):
        # OPPGAVE: Skriv SQL som sletter den gitte raden i tabellen
        self._execute_sql('''
        DELETE FROM todo WHERE id = :id
        ''', {'id': id})
