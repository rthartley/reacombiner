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