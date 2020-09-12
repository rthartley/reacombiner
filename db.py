import sqlite3
from sqlite3 import Error
import gui
import data

conn = None


def addProject(project):
    sql = ''' INSERT INTO projects(project, mix, mod_date, location, tempo, record_path, sample_rate, project_notes)
                  VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def addTrack(track):
    sql = ''' INSERT INTO tracks(project_id, number, name, main_send, vol, pan, aux_recvs, track_notes)
                      VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, track)
    conn.commit()
    return cur.lastrowid


def addItem(item):
    sql = ''' INSERT INTO items(project_num, track_id, item_id, name, source, position, file)
                          VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, item)
    conn.commit()
    return cur.lastrowid


def addPlugin(item):
    sql = ''' INSERT INTO plugins(project_num, track_id, plugin_id, name, file, preset)
                          VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, item)
    conn.commit()
    return cur.lastrowid


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
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


def createTable(create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def dropTables():
    cursor = conn.cursor()
    cursor.execute('DROP TABLE projects')
    conn.commit()
    cursor.execute('DROP TABLE tracks')
    conn.commit()
    cursor.execute('DROP TABLE items')
    conn.commit()
    cursor.execute('DROP TABLE plugins')
    conn.commit()


def createTables():
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
    createTable(sql_create_projects_table)
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
    createTable(sql_create_tracks_table)
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
    createTable(sql_create_items_table)
    print(columns_in_table('items'))
    sql_create_plugins_table = """ CREATE TABLE plugins (
                                                    id integer PRIMARY KEY,
                                                    project_num integer,
                                                    track_id integer,
                                                    plugin_id integer,
                                                    name text NOT NULL,
                                                    file text NOT NULL,
                                                    preset text
                                                ); """
    createTable(sql_create_plugins_table)


def loadProjects():
    sql = 'SELECT * from projects'
    cur = conn.cursor()
    cur.execute(sql)
    projects = cur.fetchall()
    cur.close()
    for project in projects:
        data.addProject(project[0], project[1:])  # include project_id
        sql = "SELECT * FROM tracks where project_id = " + str(project[0])
        cur = conn.cursor()
        cur.execute(sql)
        tracks = cur.fetchall()
        cur.close()
        for track in tracks:
            data.addTrack(track[1], track[2], track[3:])  # remove track_id, but include project_id and track_num
            sql = "SELECT * FROM items where project_num = " + str(project[0]) + " AND track_id = " + str(track[2])
            cur = conn.cursor()
            cur.execute(sql)
            items = cur.fetchall()
            cur.close()
            for item in items:
                data.addItem(item[1], item[2], item[3], item[4:])
            sql = "SELECT * FROM plugins where project_num = " + str(project[0]) + " AND track_id = " + str(track[2])
            cur = conn.cursor()
            cur.execute(sql)
            plugins = cur.fetchall()
            cur.close()
            for plugin in plugins:
                data.addPlugin(plugin[1], plugin[2], plugin[3], plugin[4:])
    # finally show just the project data
    gui.showProjects(data.projectTableData)


def close():
    conn.close()
