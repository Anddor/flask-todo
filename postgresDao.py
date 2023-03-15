from daoInterface import DaoInterface
import psycopg2


class PostgresDAO(DaoInterface):
    def __init__(self, connection_string):
        self.connectionString = connection_string
        self.setup_database()
        pass

    def _execute(self, sql, params):
        conn = psycopg2.connect(self.connectionString)
        cur = conn.cursor()
        cur.execute(sql, params)
        records = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return records

    def setup_database(self):
        self._execute(
            '''CREATE TABLE IF NOT EXISTS todo (id SERIAL PRIMARY KEY, task TEXT, fav INTEGER)''', {})

    def get(self, id):
        todo = self._execute('''SELECT id, task, fav FROM todo WHERE id = %(id)s RETURNING *''',
                             {'id': id})
        return todo[0]

    def get_all(self):
        pass

    def insert(self, obj):
        pass

    def update(self, obj):
        pass

    def delete(self, id):
        pass
