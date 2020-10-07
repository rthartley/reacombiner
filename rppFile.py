import os
import time

import rpp
import PySimpleGUI as sg
from pathlib import Path, PurePosixPath

import gui


def printStructR(children, indent):
    """
     Only used in testing
    :param children: node children
    :param indent: number of spaces
    :return:
    """
    for child in children:
        if isinstance(child, sg.Element):
            print("%sElement %s %s" % ((" " * indent), child.tag, child.attrib))
            gc = child.findall('*')
            printStructR(gc, indent + 3)
        else:
            print("%s%s" % ((" " * indent), child))


def printStruct(struct):
    """
    Only used in testing
    :param struct: Whta is returned by rpp.load
    :return:
    """
    children = struct.findall('*')
    print("%s children" % len(struct))
    printStructR(children, 0)


def openFile(fn):
    if fn != '':
        try:
            with open(fn, 'r') as file:
                try:
                    projectFile = rpp.load(file)
                except (UnicodeDecodeError, ValueError, RuntimeError):
                    gui.errorMsg('Could not parse this file')
                    return None
                return projectFile
        except IOError:
            gui.errorMsg('Could not open this file')
            return None
        except:
            gui.errorMsg("An unknown error occurred")
            return None


def getFileDetails(fname):
    ct = time.ctime(os.path.getmtime(fname))
    path = PurePosixPath(fname)
    location = str(path.parent.parent)
    dir = path.parent.stem
    basen = path.stem
    return [dir, basen, ct, location]
