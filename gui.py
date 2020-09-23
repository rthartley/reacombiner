import os
import subprocess
from pathlib import PurePath
from time import strptime, mktime

import file_utils
from data import Projects, Project, Track, Item, Plugin

import PySimpleGUI as sg
import rpp
import db
import rppFile
import data

sg.ChangeLookAndFeel('LightGreen')
sg.SetOptions(element_padding=(5, 5))
bg_color = "cadetblue"

allProjects: Projects;

# ------ Menu Definition ------ #
menu_def = [['File', ['Add Project', 'Delete Project', 'Print Project', 'Exit']],
            ['Run', ['Run Reaper']],
            ['Help', 'About...']]

projectTableHeadings = [sg.Button('Project'), sg.Button('Mix'), sg.Button('Last Modified')]
projectTable = sg.Table([], auto_size_columns=False,
                        col_widths=[20, 12, 20], justification="left",
                        key='PROJECTS', num_rows=15, enable_events=True,
                        headings=[b.get_text() for b in projectTableHeadings])
projectSorts = [[sg.Text('Sort by', justification='r'),
                 sg.Radio('Name', 'sort', default=True, size=(12, 1), key='-SORT-NAME-', enable_events=True),
                 sg.Radio('Mix', 'sort', size=(12, 1), key='-SORT-MIX-', enable_events=True),
                 sg.Radio('Date', 'sort', size=(12, 1), key='-SORT-DATE-', enable_events=True)]]
projectTexts = [
    [sg.Text('Location', justification='r', pad=((0, 10), (15, 5))),
     sg.Text(size=(45, 2), key='location', auto_size_text=True, background_color=bg_color, pad=((0, 0), (15, 5)))],
    [sg.Text('Tempo', justification='r', pad=((0, 10), (0, 5))),
     sg.Text(size=(20, 1), key='tempo', background_color=bg_color, pad=((0, 0), (0, 5)))],
    [sg.Text('Record Path', justification='r', pad=((0, 10), (0, 0))),
     sg.Text(size=(45, 2), key='record_path', auto_size_text=True, background_color=bg_color, pad=((0, 0), (0, 5)))],
    [sg.Text('Sample Rate', justification='r', pad=((0, 10), (0, 0))),
     sg.Text(size=(10, 1), key='sample_rate', background_color=bg_color, pad=((0, 0), (0, 5)))],
    [sg.Frame("Project Notes",
              [[sg.Text(size=(40, 10),
                        key='project_notes', auto_size_text=True, background_color=bg_color)]], pad=((0, 0), (15, 15)),
              )]]
projectTableLayout = [[projectTable]] + projectSorts + projectTexts

trackTableHeadings = ['Num', 'Track Name']
trackTable = sg.Table([], max_col_width=15, auto_size_columns=False, num_rows=15,
                      col_widths=[4, 25], justification="left",
                      key='TRACKS', enable_events=True, headings=trackTableHeadings)
trackTexts = [[sg.Text('Main Send', justification='r', pad=((0, 10), (15, 5))),
               sg.Text(size=(5, 1), key='main_send', background_color=bg_color, pad=((0, 0), (15, 5)))],
              [sg.Text('Vol', justification='r', pad=((0, 10), (0, 5))),
               sg.Text(size=(10, 1), key='vol', background_color=bg_color, pad=((0, 0), (0, 5)))],
              [sg.Text('Pan', justification='r', pad=((0, 10), (0, 5))),
               sg.Text(size=(10, 1), key='pan', background_color=bg_color, pad=((0, 0), (0, 5)))],
              [sg.Text('Aux Recvs', justification='r', pad=((0, 10), (0, 5))),
               sg.Text(size=(25, 5), key='aux_recvs', background_color=bg_color, pad=((0, 0), (0, 5)))],
              [sg.Frame("Track Notes", [[sg.Text(size=(40, 8), key='track_notes', background_color=bg_color)]],
                        pad=((0, 0), (15, 15)))]]
trackTableLayout = [[trackTable]] + trackTexts

itemTableHeadings = ['Item Name', 'Source', 'Position']
itemTable = sg.Table([], auto_size_columns=False, num_rows=15, key='ITEMS', enable_events=True,
                     col_widths=[25, 6, 20], justification="left", headings=itemTableHeadings)
pluginTableHeadings = ['Name', 'File', 'Preset']
pluginTable = sg.Table([], max_col_width=15, auto_size_columns=False, num_rows=15,
                       col_widths=(24, 12, 12), key='PLUGINS', headings=pluginTableHeadings,
                       justification="left")
pluginTableLayout = [[pluginTable]]
itemTexts = [
    [sg.Text('File', justification='r', pad=((0, 10), (15, 0))),
     sg.Text(size=(40, 2), auto_size_text=True, background_color=bg_color, key='file', pad=((0, 0), (15, 0)))],
    [sg.Frame('Plugins', [[pluginTable]], pad=(10, 10))]]
itemTableLayout = [[itemTable]] + itemTexts

# ------ GUI Definition ------ #
layout = [
    [sg.Menu(menu_def, )],
    [
        sg.Frame('Projects', projectTableLayout, pad=((0, 10), (0,)), vertical_alignment='top'),
        sg.Frame('Tracks', trackTableLayout, vertical_alignment='top', pad=((0, 10), (0, 0))),
        sg.Frame('Items', itemTableLayout, vertical_alignment='top')],
]


def newAddNewProject():
    fname = file_utils.browseFile()
    print(fname[0])
    projectFile = rppFile.openFile(fname[0])
    if projectFile is None:
        return
    #    rppFile.printStruct(projectFile)
    dtls = rppFile.getFileDetails(fname[0])
    dtls.append(projectFile.find('TEMPO')[1])
    dtls.append(projectFile.find('RECORD_PATH')[1])
    dtls.append(projectFile.find('SAMPLERATE')[1])
    notes = projectFile.find('NOTES')
    if notes is not None:
        txt = "\n".join([notes[n][1:] for n in range(0, len(notes))])
    else:
        txt = ""
    dtls.append(txt)
    newProject = Project(allProjects.maxProjectNum + 1, dtls[0], dtls[1], dtls[2], dtls[3], dtls[4], dtls[5], dtls[6],
                         dtls[7])
    if allProjects.findProject(newProject):
        sg.popup_error("Project exists")
        return
    pnum = db.addProject(dtls)
    allProjects.addProject(newProject)
    updateProjects(sorted(allProjects.getProjects(), key=lambda proj: proj.name))
    tracks = projectFile.findall('TRACK')
    print('Project has %d tracks' % len(tracks))
    clearTables()
    for n in range(0, len(tracks)):
        track = tracks[n]
        tnum = n + 1
        trackDtls = [track.find('NAME')[1], track.find('MAINSEND')[1], track.find('VOLPAN')[1],
                     track.find('VOLPAN')[2],
                     ",".join([lst[1] for lst in track.findall('AUXRECV')])]
        tnotes = track.find('S&M_TRACKNOTES')
        if tnotes is not None:
            txt = "\n".join([tnotes[n][1:] for n in range(0, len(tnotes))])
        else:
            txt = ""
        trackDtls.append(txt)
        newTrack = data.Track(tnum, trackDtls[0], trackDtls[1], trackDtls[2], trackDtls[3], trackDtls[4], trackDtls[5])
        newProject.addTrack(newTrack)
        db.addTrack([pnum, tnum] + trackDtls)
        items = track.findall('ITEM')
        for inum in range(0, len(items)):
            item = items[inum]
            src = item.find('SOURCE')
            itemDtls = [item.find('NAME')[1], src.attrib[0], item.find('POSITION')[1]]
            fl = src.find('FILE')
            if fl is not None:
                itemDtls.append(fl[1])
            else:
                itemDtls.append('')
            newItem = data.Item(inum, itemDtls[0], itemDtls[1], itemDtls[2], itemDtls[3])
            newTrack.addItem(newItem)
            db.addItem([pnum, tnum, inum] + itemDtls)
        fxchain = track.find('FXCHAIN')
        if fxchain is not None:
            preset = None
            vst = None
            items = fxchain.find('.')
            for inum in range(0, len(items)):
                item = items[inum]
                if isinstance(item, list) and item[0] == 'PRESETNAME' and vst is not None:
                    preset = item[1]
                    print('PRESETNAME=' + item[1] + ' goes with VST ' + str(vst))
                    pluginDtls = [vst[0], vst[1], item[1]]
                    newPlugin = data.Plugin(inum, pluginDtls[0], pluginDtls[1], pluginDtls[2])
                    newTrack.addPlugin(newPlugin)
                    db.addPlugin([pnum, tnum, inum] + pluginDtls)
                    vst = None
                elif isinstance(item, rpp.element.Element):
                    if item.tag == 'VST':
                        if vst is not None:
                            pluginDtls = [vst[0], vst[1], '']
                            newPlugin = data.Plugin(inum, pluginDtls[0], pluginDtls[1], pluginDtls[2])
                            newTrack.addPlugin(newPlugin)
                            db.addPlugin([pnum, tnum, inum] + pluginDtls)
                        vst = item.attrib[0:2]
                        print('VST=' + str(vst))
            if vst is not None:
                pluginDtls = [vst[0], vst[1], '']
                newPlugin = data.Plugin(inum, pluginDtls[0], pluginDtls[1], pluginDtls[2])
                newTrack.addPlugin(newPlugin)
                db.addPlugin([pnum, tnum, inum] + pluginDtls)


def deleteOldProject(project: Project):
    if 'OK' == sg.popup_ok_cancel(" Are you absolutely sure? - there is no undo"):
        pnum = project.projectNum
        db.deleteProject(pnum)
        allProjects.deleteProject(pnum)
        clearTables()
        projectTable.update([[project.name, project.mix, project.date] for project in allProjects.getProjects()])


def createMyWindow():
    global window0
    window0 = sg.Window("ReaCombiner", layout, default_element_size=(12, 1),
                       auto_size_text=False, auto_size_buttons=False,
                       default_button_element_size=(12, 1),
                       finalize=True, resizable=True)
    window0.Hide()


def chunk(lst, upto):
    ret = ""
    while len(",".join(lst)) > upto:
        n = 0
        while len(",".join(lst[0:n])) < upto:
            n += 1
        ret += ",".join(lst[0:n])
        ret += '\n'
        lst = lst[n:]
    ret += ",".join(lst)
    return ret


def chunkStr(str, upto):
    ret = ""
    while len(str) > upto:
        ret += str[:upto] + '\n'
        str = str[upto:]
    ret += str
    return ret


def clearTables():
    window0.find_element('main_send').update('')
    window0.find_element('vol').update('')
    window0.find_element('pan').update('')
    window0.find_element('aux_recvs').update('')
    window0.find('file').update('')
    data.newShowTracks(trackTable, None)
    data.newShowItems(itemTable, None)
    data.newShowPlugins(pluginTable, None)


def epochSecs(dt: str):
    t = strptime(dt)
    return mktime(t)


def updateProjects(sps: list):
    global allProjects
    allProjects.projects = sps
    projectTable.update([p.getProjectDetails() for p in sps])
    clearTables()


def showMyWindow(projects: Projects):
    global allProjects
    allProjects = Projects()
    updateProjects(sorted(projects.getProjects(), key=lambda proj: proj.name))
    window = window0
    window.UnHide()

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        # ------ Process menu choices ------ #
        if event == 'About...':
            with open("README.txt", "r", encoding="utf-8") as input_file:
                layout = [[sg.Multiline(input_file.read(), size=(80, 25), autoscroll=True, key='_OUTPUT_')],
                          [sg.Button('OK', key='_OK_')]]
                window1 = sg.Window('Help').Layout(layout)
                window.Hide()
                window = window1
                window1.Read(timeout=0)
        elif event == '_OK_':
            window.Hide()
            window = window0
            window0.UnHide()
        elif event == 'Run Reaper':
            print(event)
            if len(values['PROJECTS']) > 0:
                row = values['PROJECTS'][0]
                project = allProjects.getProject(row)
                path = PurePath(project.location, project.name, project.mix + '.rpp')
                env = os.environ.copy()
                subprocess.Popen(['reaper', str(path)], env=env)
            else:
                sg.popup_error('First select a project to run')
        elif event == 'Add Project':
            newAddNewProject()
        elif event == 'Delete Project':
            print(event)
            if len(values['PROJECTS']) > 0:
                row = values['PROJECTS'][0]
                project = allProjects.getProject(row)
                deleteOldProject(project)
            else:
                sg.popup_error('First select a project to run')
        elif event == 'Print Project':
            print(event)
            if len(values['PROJECTS']) > 0:
                row = values['PROJECTS'][0]
                project = allProjects.getProject(row)
                project.print()
            else:
                sg.popup_error('First select a project to run')
        elif event == 'PROJECTS':
            print(values['PROJECTS'])
            if len(values['PROJECTS']) > 0:
                row = values['PROJECTS'][0]
                project = allProjects.getProject(row)
                window.find_element('location').update(chunkStr(project.location, 50))  # 50 is text width
                window.find_element('tempo').update(project.tempo)
                window.find_element('record_path').update(
                    chunkStr(project.recordPath, 50))  # 50 is text width
                window.find_element('sample_rate').update(project.sampleRate)
                window.find_element('project_notes').update(project.projectNotes)
                clearTables()
                data.newShowTracks(trackTable, project)
        elif event == 'TRACKS':
            print(values['TRACKS'])
            if len(values['PROJECTS']) > 0 and len(values['TRACKS']) > 0:
                prow = values['PROJECTS'][0]
                project = allProjects.getProject(row)
                trow = values['TRACKS'][0]
                tracks = project.getTracks()
                trackNum = trackTable.get()[trow][0]
                track = tracks[trackNum]
                window.find_element('main_send').update(track.mainSend)
                window.find_element('vol').update(track.vol)
                window.find_element('pan').update(track.pan)
                ar = window.find_element('aux_recvs')
                lst = track.auxReceives.split(",")
                if lst == ['']:
                    mstr = ''
                else:
                    mstr = chunk([str(int(n) + 1) for n in lst], 25)  # 25 is width of aux_recvs
                ar.update(mstr)
                window.find_element('track_notes').update(track.trackNotes)
                data.newShowItems(itemTable, track)
                data.newShowPlugins(pluginTable, track)
        elif event == 'ITEMS':
            print(values['ITEMS'])
            if len(values['PROJECTS']) > 0 and len(values['TRACKS']) > 0 and len(values['ITEMS']) > 0:
                prow = values['PROJECTS'][0]
                project = allProjects.getProject(row)
                trow = values['TRACKS'][0]
                tracks = project.getTracks()
                trackNum = trackTable.get()[trow][0]
                track = tracks[trackNum]
                irow = values['ITEMS'][0]
                window.find_element('file').update(chunkStr(track.getItems()[irow].file, 50))
        elif event == '-SORT-NAME-':
            updateProjects(sorted(allProjects.getProjects(), key=lambda proj: proj.name))
        elif event == '-SORT-MIX-':
            updateProjects(sorted(allProjects.getProjects(), key=lambda proj: proj.mix))
        elif event == '-SORT-DATE-':
            updateProjects(sorted(allProjects.getProjects(), key=lambda proj: epochSecs(proj.date)))
        else:
            print(event, values)
    window.close()
    db.close()
