import unittest
from unittest.mock import Mock

import PySimpleGUI as sg
import db
import os

import file_utils
from data import Project, Projects
from gui import addNewProject, projectTable, createMyWindow


class DbTestCase(unittest.TestCase):

    def create_db_file(self):
        self.db_file = 'test_sqlitedb'
        open(self.db_file, 'w+').close()

    def create_db(self):
        self.conn = db.createConnection(self.db_file)

    def close_and_delete(self):
        self.conn.close()
        os.remove(self.db_file)

    def create_error_mock(self):
        self.mock = Mock()
        sg.popup_error = self.mock

    def test_file_exists(self):
        self.create_error_mock()
        ret = db.createConnection('abcd.def')
        self.assertIsNone(ret)

    def test_connection_ok(self):
        self.create_error_mock()
        self.create_db_file()
        self.create_db()
        self.assertIsNotNone(self.conn)
        self.close_and_delete()

    # noinspection SpellCheckingInspection
    def test_create_table(self):
        self.create_error_mock()
        self.create_db_file()
        self.create_db()
        db.createTable(db.sql_create_projects_table)
        self.mock.assert_not_called()
        self.close_and_delete()

    def test_insert_into_table(self):
        self.create_error_mock()
        self.create_db_file()
        self.create_db()
        db.createTable(db.sql_create_projects_table)
        project = ('P1', 'Mix1', 'date', 'loc', '', '', '', '')
        row = db.addProject(project)
        self.assertEqual(row, 1)
        self.mock.assert_not_called()
        self.close_and_delete()

    def test_retrieve_from_table(self):
        self.create_error_mock()
        self.create_db_file()
        self.create_db()
        db.createTable(db.sql_create_projects_table)
        project = ('P1', 'Mix1', 'date', 'loc', '', '', '', '')
        row = db.addProject(project)
        sql = 'SELECT * from projects'
        cur = self.conn.cursor()
        cur.execute(sql)
        projects = cur.fetchall()
        cur.close()
        self.assertEqual(projects[0][1], 'P1')
        self.mock.assert_not_called()
        self.close_and_delete()

    def test_delete_from_table(self):
        self.create_error_mock()
        self.create_db_file()
        self.create_db()
        db.createTable(db.sql_create_projects_table)
        project = ('P1', 'Mix1', 'date', 'loc', '', '', '', '')
        row = db.addProject(project)
        sql = ' DELETE FROM projects WHERE id = ' + str(1)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        self.mock.assert_not_called()
        sql = 'SELECT * from projects'
        cur = self.conn.cursor()
        cur.execute(sql)
        projects = cur.fetchall()
        cur.close()
        self.assertEqual(len(projects), 0)
        self.close_and_delete()

    def test_all_plugin_types(self):
        self.create_db_file()
        self.create_db()
        db.createTables()
        self.mock = Mock(return_value=['test-plugins.RPP'])
        createMyWindow()  # could be mocked?
        file_utils.browseFile = self.mock
        newAddNewProject()
        sql = "SELECT * FROM plugins "
        cur = db.conn.cursor()
        cur.execute(sql)
        plugins = cur.fetchall()
        cur.close()
        self.assertEqual(len(plugins), 7)


if __name__ == '__main__':
    unittest.main()
