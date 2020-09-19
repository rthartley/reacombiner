import gui
import db


if __name__ == '__main__':
    db.createConnection('c:/Users//Roger.AMD-ONE/sqlitedb')
    gui.createMyWindow()
#    db.loadProjects()
    tempProjects = db.loadProjects()
    gui.showMyWindow(tempProjects)
