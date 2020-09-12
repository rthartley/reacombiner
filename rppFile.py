import os
import time

import rpp
import PySimpleGUI as sg
from pathlib import Path, PurePosixPath


def printStructR(children, indent):
    for child in children:
        if isinstance(child, sg.Element):
            print("%sElement %s %s" % ((" " * indent), child.tag, child.attrib))
            gc = child.findall('*')
            printStructR(gc, indent + 3)
        else:
            print("%s%s" % ((" " * indent), child))


def printStruct(struct):
    children = struct.findall('*')
    print("%s children" % len(struct))
    printStructR(children, 0)


def openFile(fn):
    with open(fn, 'r') as file:
        projectFile = rpp.load(file)
        return projectFile


def browseFile():
    event, values = sg.Window('Open RPP file',
                              [[sg.Text('Document to open')],
                               [sg.In(), sg.FileBrowse()],
                               [sg.Open(), sg.Cancel()]]).read(close=True)
    return values


def getFileDetails(fname):
    ct = time.ctime(os.path.getmtime(fname))
    path = PurePosixPath(fname)
    location = str(path.parent.parent)
    dir = path.parent.stem
    basen = path.stem
    return [dir, basen, ct, location]