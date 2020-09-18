import os
import sqlite3


class DBOpen:
    """
    Simple CM for sqlite3 databases. Commits everything at exit.
    """

    def __init__(self, path):
        self.path = path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        assert os.path.exists(self.path), 'Database file now found.'
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


class SQLiteTool:
    """
    Tool for work with SQLite database
    https://docs.python.org/3/library/sqlite3.html
    """

    def __init__(self, path: str = ''):
        """Specify database file path. Creates DB in memory by default"""

        self.path = path or ':memory:'

    def __str__(self):
        return f'DB path: {self.path}'

    def connect(self):
        """ Connect to database and return connection. Creates database if does not exists """

        return sqlite3.connect(self.path)

    def get_cursor(self):
        return self.connect().cursor()

    @staticmethod
    def _scrub(table_name):
        """Clean table name to use only A-Z a-z 0-9 for secure."""

        return ''.join(char for char in table_name if char.isalnum())

    def execute(self, cmd):
        """Execute custom SQL query using different actions.

        Example1: "INSERT INTO DtoClusterSettings VALUES ('test', null , 'Auto', '172.16.0.1')")\n
        Example2: "INSERT INTO present VALUES('test2', ?, 10)", (None,)

        :param cmd: Query to execute
        :type cmd: str
        :return: str(cmd)
        """
        with DBOpen(self.path) as cursor:
            cursor.execute(cmd)
            return cmd

    def select(self, table, order='Uid', limit=1, last=False, column=None):
        """
        SELECT * FROM 'table' ORDER BY

        :param limit:
        :param table:
        :param order:
        :param last:
        :return:
        """

        table_name = self._scrub(table)
        select = '*' if not column else self._scrub(column)

        with DBOpen(self.path) as cursor:
            if last:
                cursor.execute(f'SELECT {select} FROM {table_name} ORDER BY :order DESC LIMIT :limit',
                               {'order': order, 'limit': limit})
                return cursor.fetchone()
            cursor.execute(f'SELECT {select} FROM {table_name} ORDER BY ?', (order,))
            return cursor.fetchall()

    def select_last_row(self, table, order='Uid', limit=1):
        """

        :param table:
        :param order:
        :param limit:
        :return:
        """

        table_name = self._scrub(table)
        with DBOpen(self.path) as cursor:
            cursor.execute(f'SELECT * FROM {table_name} ORDER BY :order DESC LIMIT :limit',
                           {'order': order, 'limit': limit})
            return cursor.fetchone()

    def delete(self, table, rowid='last', order='Uid'):
        """
        :Action: Delete record by ID or last row(if absent params)
        :Parameters: IP, id, table
        """

        table_name = self._scrub(table)
        with DBOpen(self.path) as cursor:
            cursor.execute(f'SELECT * FROM {table_name} ORDER BY :order DESC LIMIT 1',
                           {'order': order, })

            rows = cursor.fetchone()

            if not rows:
                return 'Table is empty'

            if rowid == 'last':
                last_id = rows[0]
                cursor.execute(f'DELETE FROM {table_name} WHERE {order}=?', (last_id,))

            else:
                cursor.execute(f'DELETE FROM {table_name} WHERE {order}=?', rowid)

    def insert(self, table, args):
        """
        Insert into table. For args use tuple

        :param table: name of table, default 'ReplicationItem'
        :type table: str
        :param args: Tuple of args
        :type args: tuple
        :return:
        """

        table_name = self._scrub(table)  # Clean table name from spec symbols
        n = len(args)  # Get number of parameters
        placeholders = ('?, ' * n)[:-2]  # Generate "?" placeholders for parameters

        with DBOpen(self.path) as cursor:
            try:
                cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", args)
            except sqlite3.IntegrityError as err:
                return f'Error: {err}'
            return 'Table name:', table, 'parameters:', args

    def insert_many(self, table, queries):
        """
        Insert several rows into one table.

        :param table: Table name
        :type table: str
        :param queries: List of queries to the same table
        :type queries: list
        :return:
        """

        for query in queries:
            self.insert(table, query)
        return 'Table name:', table, 'parameters:', queries

    def update(self, table):

        self._scrub(table)  # Clean table name from spec symbols
        with DBOpen(self.path):
            try:
                # UPDATE ExampleTable SET age = 18 WHERE age = 17
                raise NotImplementedError
                # cursor.execute(f"UPDATE {table_name} SET ({placeholders})", args)
            except sqlite3.IntegrityError as err:
                return f'Error: {err}'
            # return 'Table name:', table, 'parameters:', args
