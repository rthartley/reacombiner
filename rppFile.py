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
    if fn != '':
        with open(fn, 'r') as file:
            try:
                projectFile = rpp.load(file)
            except (UnicodeDecodeError, ValueError, RuntimeError):
                sg.popup_error('Could not parse this file')
                return None
            return projectFile



def getFileDetails(fname):
    ct = time.ctime(os.path.getmtime(fname))
    path = PurePosixPath(fname)
    location = str(path.parent.parent)
    dir = path.parent.stem
    basen = path.stem
    return [dir, basen, ct, location]
