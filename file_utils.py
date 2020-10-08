import os

import PySimpleGUI as sg

lastBrowseDir = ''


def browseDir(title: str):
    event, values = sg.Window(title,
                              [[sg.Text('Folder to open')],
                               [sg.In(lastBrowseDir), sg.FolderBrowse()],
                               [sg.Open(), sg.Cancel()]]).read(close=True)
    return values[0]


def browseFile():
    event, values = sg.Window('Open RPP file',
                              [[sg.Text('Document to open')],
                               [sg.In(), sg.FileBrowse()],
                               [sg.Open(), sg.Cancel()]]).read(close=True)
    return values


def scrapeDirectory():
    dir = browseDir('Scrape folder')
    files = []
    for r, d, f in os.walk(dir):
        for file in f:
            if file.endswith(".rpp"):
                #  print(os.path.join(r, file).replace('\\', '/'))
                files.append(os.path.join(r, file).replace('\\', '/'))
    return files


def selectProjects(files):
    rows = [[sg.Checkbox('', pad=(0, 0)), sg.Text(text=f, pad=(0, 0))] for f in files]
    event, values = sg.Window('Select RPP files',
                              [[sg.Column(rows, size=(500, 500), scrollable=True)],
                               [sg.Open(), sg.Cancel()]]
                              ).read(close=True)
    return [files[i] for i in range(0, len(values)) if values[i]]


def errorMsg(msg):
    sg.popup_error(msg, title='Error', modal=True)
