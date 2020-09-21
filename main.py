import os
import PySimpleGUI as sg

import file_utils
import gui
import db


def getHome():
    if 'HOME' in os.environ:
        return  os.environ['HOME']
    elif 'USERPROFILE' in os.environ:
        return os.environ['USERPROFILE']
    else:
        return file_utils.browseDir('DB location')



if __name__ == '__main__':
    db.createConnection(getHome().replace('\\', '/') + '/sqlitedb')
    gui.createMyWindow()
    gui.showMyWindow(db.loadProjects())
