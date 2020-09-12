import db
import PySimpleGUI as sg

projectTableData = {}
trackTableData = {}
itemTableData = {}
pluginTableData = {}


def addProject(pnum, projectData):
    if projectData not in projectTableData.values():
        projectTableData[pnum] = projectData
    else:
        sg.popup_error('Project already exists')


def addTrack(pnum, tnum, trackData):
    if pnum not in trackTableData.keys():
        trackTableData[pnum] = {}
    trackTableData[pnum][tnum] = trackData


def addItem(pnum, tnum, inum, itemData):
    if pnum not in itemTableData.keys():
         itemTableData[pnum] = {}
    if tnum not in itemTableData[pnum].keys():
        itemTableData[pnum][tnum] = {}
    itemTableData[pnum][tnum][inum] = itemData


def addPlugin(pnum, tnum, vnum, pluginData):
    if pnum not in pluginTableData.keys():
         pluginTableData[pnum] = {}
    if tnum not in pluginTableData[pnum].keys():
        pluginTableData[pnum][tnum] = {}
    pluginTableData[pnum][tnum][vnum] = pluginData


def showTracks(table, pnum):
    if pnum not in trackTableData:
        table.update([])
    else:
        data = []
        keys = sorted(trackTableData[pnum].keys())
        for n in range(0, len(keys)):
            data.append([n + 1] + list(trackTableData[pnum][keys[n]][0:2]))
        table.update(data)


def showItems(table, pnum, tnum):
    if pnum not in itemTableData or tnum not in itemTableData[pnum]:
        table.update([])
    else:
        table.update(itemTableData[pnum][tnum].values())


def showPlugins(table, pnum, tnum):
    if pnum not in pluginTableData or tnum not in pluginTableData[pnum]:
        table.update([])
    else:
        table.update(pluginTableData[pnum][tnum].values())


def update(textElem, pnum, n):
    textElem.update(projectTableData[pnum][n])
