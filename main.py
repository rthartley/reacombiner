import rppFile
import gui
import db

if __name__ == '__main__':
    db.createConnection('/home/roger/sqlitedb')
    gui.createMyWindow()
    projects = db.loadProjects()
    gui.showMyWindow()
