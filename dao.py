import contextlib
import os
import sqlite3

DATABASE_FILE = 'database.db'


class TodoDAO(object):
    def __init__(self):
        # self.setup_database()
        pass

    """
    Kjører SQL-spørringen 'statement' med gitte verdi-bindinger 'values'
    """

    def _execute_sql(self, statement, values):
        with contextlib.closing(sqlite3.connect(DATABASE_FILE)) as conn:  # auto-closes
            with conn:  # auto-commits
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

    def _map_todo(self, todo_row):
        return {
            'id': todo_row[0],
            'task': todo_row[1],
            'fav': todo_row[2]
        }

    """
    Opprett tabeller i databasen om database-filen ikke finnes fra før.
    """

    def setup_database(self):
        if not os._exists(DATABASE_FILE):  # python compatiblity
            # OPPGAVE: Skriv SQL som oppretter en tabell med feltene i en todo:

            self._execute_sql('''CREATE TABLE todo (id INTEGER PRIMARY KEY, task TEXT, fav INTEGER)
            ''', {})

    def get_all(self):
        return_list = []
        # fetch all todos from database

        todos = self._execute_sql_fetchall(
            '''SELECT id, task, fav FROM todo''', {})
        for todo in todos:
            return_list.append(self._map_todo(todo))
        return return_list

    def get(self, id):

        # fetch the todo with the given id
        todo = self._execute_sql('''SELECT id, task, fav FROM todo WHERE id = :id''',
                                 {'id': id})
        return self._map_todo(todo)

    def create(self, data):
        todo = data
        # OPPGAVE: Skriv SQL som setter inn en ny rad i todo tabellen
        todo_id = self._execute_sql_lastrowid('''
        INSERT INTO todo (task, fav) VALUES (:task, :fav)
        ''', data)

        todo['id'] = todo_id
        return todo

    def update(self, id, data):
        # OPPGAVE: Skriv SQL som oppdaterer den gitte raden i tabellen
        self._execute_sql('''
        UPDATE todo SET task = :task, fav = :fav WHERE id = :id
        ''', data)
        return data

    def delete(self, id):
        # OPPGAVE: Skriv SQL som sletter den gitte raden i tabellen
        self._execute_sql('''
        DELETE FROM todo WHERE id = :id
        ''', {'id': id})