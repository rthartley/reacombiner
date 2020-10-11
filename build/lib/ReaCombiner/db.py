import os
import sqlite3
from sqlite3 import Error
import PySimpleGUI as sg
from ReaCombiner import data
from ReaCombiner import gui

conn = None

sql_create_projects_table = """ CREATE TABLE projects (
                                     id integer PRIMARY KEY,
                                     project text NOT NULL,
                                     mix text NOT NULL,
                                     mod_date text,
                                     location text,
                                     tempo text,
                                     record_path text,
                                     sample_rate text,
                                     project_notes text
                                 ); """

sql_create_tracks_table = """ CREATE TABLE tracks (
                                         id integer PRIMARY KEY,
                                         project_id integer,
                                         number integer,
                                         name text NOT NULL,
                                         main_send text,
                                         vol text,
                                         pan text,
                                         aux_recvs,
                                         track_notes text
                                     ); """

sql_create_items_table = """ CREATE TABLE items (
                                            id integer PRIMARY KEY,
                                            project_num integer,
                                            track_id integer,
                                            item_id integer,
                                            name text NOT NULL,
                                            source text NOT NULL,
                                            position real,
                                            file text
                                        ); """

sql_create_plugins_table = """ CREATE TABLE plugins (
                                                id integer PRIMARY KEY,
                                                project_num integer,
                                                track_id integer,
                                                plugin_id integer,
                                                name text NOT NULL,
                                                file text NOT NULL,
                                                preset text
                                            ); """


def addProject(project):
    sql = ''' INSERT INTO projects(project, mix, mod_date, location, tempo, record_path, sample_rate, project_notes)
                  VALUES(?,?,?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, project)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        gui.errorMsg("Could not add project")
        raise e


def addTrack(track):
    sql = ''' INSERT INTO tracks(project_id, number, name, main_send, vol, pan, aux_recvs, track_notes)
                      VALUES(?,?,?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, track)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        gui.errorMsg("Could not add track")
        raise e


def addItem(item):
    sql = ''' INSERT INTO items(project_num, track_id, item_id, name, source, position, file)
                          VALUES(?,?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, item)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        gui.errorMsg("Could not add item")
        raise e


def addPlugin(item):
    sql = ''' INSERT INTO plugins(project_num, track_id, plugin_id, name, file, preset)
                          VALUES(?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, item)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        gui.errorMsg("Could not add plugin")
        raise e


def tables_in_sqlite_db():
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    cursor.close()
    return tables


def columns_in_table(tablename):
    cursor = conn.execute("PRAGMA table_info(" + tablename + ")")
    columns = cursor.fetchall()
    cursor.close()
    return columns


def createConnection(db_file):
    """ create a database connection to a SQLite database """
    global conn
    try:
        if os.path.isfile(db_file):
            conn = sqlite3.connect(db_file)
        else:
            gui.errorMsg('Could not find database file')
            return None
        # print(sqlite3.version)
    except Error as e:
        # print(e)
        gui.errorMsg('Could not contact database - quitting')
        return None
    return conn


def createTable(create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        gui.errorMsg('Error creating table: ' + str(e))
        # print(e)


def dropTables():
    try:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE projects')
        conn.commit()
        cursor.execute('DROP TABLE tracks')
        conn.commit()
        cursor.execute('DROP TABLE items')
        conn.commit()
        cursor.execute('DROP TABLE plugins')
        conn.commit()
    except sqlite3.OperationalError:
        pass


def createTables():
    createTable(sql_create_projects_table)
    createTable(sql_create_tracks_table)
    createTable(sql_create_items_table)
    print(columns_in_table('items'))
    createTable(sql_create_plugins_table)


def loadProjects():
    sql = 'SELECT * from projects'
    cur = conn.cursor()
    cur.execute(sql)
    projects = cur.fetchall()
    cur.close()
    tempProjects = data.Projects()
    maxProjectNum = 0
    for project in projects:
        projectNum = project[0]
        maxProjectNum = max(maxProjectNum, projectNum)
        tempProject = data.Project(project[0], project[1], project[2], project[3], project[4], project[5], project[6],
                                   project[7], project[8])
        tempProjects.addProject(tempProject)
    tempProjects.maxProjectNum = maxProjectNum
    sql = "SELECT * FROM tracks "
    cur = conn.cursor()
    cur.execute(sql)
    tracks = cur.fetchall()
    cur.close()
    for track in tracks:
        tempProject1 = tempProjects.findProjectNum(track[1])
        tempTrack1 = data.Track(track[2], track[3], track[4], track[5], track[6], track[7], track[8])
        tempProject1.addTrack(tempTrack1)
    sql = "SELECT * FROM items "
    cur = conn.cursor()
    cur.execute(sql)
    items = cur.fetchall()
    cur.close()
    for item in items:
        tempProject2 = tempProjects.findProjectNum(item[1])
        tempTrack2 = tempProject2.getTrack(item[2])
        tempItem2 = data.Item(item[3], item[4], item[5], item[6], item[7])
        tempTrack2.addItem(tempItem2)
    sql = "SELECT * FROM plugins "
    cur = conn.cursor()
    cur.execute(sql)
    plugins = cur.fetchall()
    cur.close()
    for plugin in plugins:
        tempProject3 = tempProjects.findProjectNum(plugin[1])
        tempTrack3 = tempProject3.getTrack(plugin[2])
        tempPlugin3 = data.Plugin(plugin[3], plugin[4], plugin[5], plugin[6])
        tempTrack3.addPlugin(tempPlugin3)
    for project in tempProjects.getProjects():
        tracks = project.tracks
        for track in tracks.values():
            recvs = track.auxReceives.split(',')
            for recv in recvs:
                if recv == '':
                    continue
                tracks[int(recv) + 1].addSend(str(track.trackNum))
    return tempProjects


def deleteProject(pnum):
    sql = ' DELETE FROM plugins WHERE project_num = ' + str(pnum)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    sql = ' DELETE FROM items WHERE project_num = ' + str(pnum)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    sql = ' DELETE FROM tracks WHERE project_id = ' + str(pnum)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    sql = ' DELETE FROM projects WHERE id = ' + str(pnum)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def close():
    conn.close()
