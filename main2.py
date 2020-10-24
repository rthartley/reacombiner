import os

from ReaCombiner import file_utils
from ReaCombiner import gui
from ReaCombiner import db


# noinspection SpellCheckingInspection
def getHome():
    if 'HOME' in os.environ:
        return os.environ['HOME']
    elif 'USERPROFILE' in os.environ:
        return os.environ['USERPROFILE']
    else:
        return file_utils.browseDir('DB location')


if __name__ == '__main__':
    db.createConnection(getHome().replace('\\', '/') + '/sqlitedb')
    gui.createMyWindow()
    gui.showMyWindow(db.loadProjects())
