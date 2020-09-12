from xml.etree.ElementTree import Element

import PySimpleGUI as sg
import rpp

import db
import rppFile
import data

sg.ChangeLookAndFeel('LightGreen')
sg.SetOptions(element_padding=(0, 0))
bg_color="cadetblue"

# ------ Menu Definition ------ #
menu_def = [['File', ['Add Project', 'DeleteProject', 'Print Project', 'Exit']],
            ['Run', ['Run Reaper']],
            ['Help', 'About...'],
            ['Find', 'Find...']]

projectTableHeadings = ['Project', 'Take', 'Last Modified']
projectTable = sg.Table(data.projectTableData, auto_size_columns=False,
                        col_widths=[20, 12, 20], justification="left",
                        key='PROJECTS', num_rows=15, enable_events=True, headings=projectTableHeadings)
projectTexts = [
    [sg.Text('Location', justification='r', pad=((0, 10), (15, 5))),
     sg.Text(size=(50, 2), key='location', auto_size_text=True, background_color=bg_color, pad=((0, 0), (15, 5)))],
    [sg.Text('Tempo', justification='r', pad=((0, 10), (0, 5))),
     sg.Text(size=(20, 1), key='tempo', background_color=bg_color, pad=((0, 0), (0, 5)))],
    [sg.Text('Record Path', justification='r', pad=((0, 10), (0, 0))),
     sg.Text(size=(50,2), key='record_path', auto_size_text=True, background_color=bg_color, pad=((0, 0), (0, 5)))],
    [sg.Text('Sample Rate', justification='r', pad=((0, 10), (0, 0))),
     sg.Text(size=(10, 1), key='sample_rate', background_color=bg_color, pad=((0, 0), (0, 5)))],
    [sg.Frame("Project Notes",
              [[sg.Text(size=(40, 10),
                        key='project_notes', auto_size_text=True, background_color=bg_color)]], pad=((0, 0), (15, 15)),
              )]]
projectTableLayout = [[projectTable]] + projectTexts

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
              [sg.Frame("Track Notes", [[sg.Text(size=(40, 10), background_color=bg_color)]], pad=((0, 0), (15, 15)))]]
trackTableLayout = [[trackTable]] + trackTexts

itemTableHeadings = ['Item Name', 'Source', 'Position']
itemTable = sg.Table([], auto_size_columns=False, num_rows=15, key='ITEMS', enable_events=True,
                     col_widths=[25, 6, 20], justification="left", headings=itemTableHeadings)
pluginTableHeadings = ['Name', 'File', 'Preset']
pluginTable = sg.Table([], max_col_width=15, auto_size_columns=False, num_rows=15,
                         col_widths=(32, 12, 32), key='PLUGINS', headings=pluginTableHeadings)
pluginTableLayout = [[pluginTable]]
itemTexts = [
    [sg.Text('File', justification='r', pad=((0, 10), (15, 0))),
     sg.Text(size=(50, 2), auto_size_text=True, background_color=bg_color, key='file', pad=((0, 0), (15, 0)))],
    [sg.Frame('Plugins', [[pluginTable]], pad=(10, 10))]]
itemTableLayout = [[itemTable]] + itemTexts

# ------ GUI Definition ------ #
layout = [
    [sg.Menu(menu_def, )],
    [
        sg.Frame('Projects', projectTableLayout, vertical_alignment='top'),
        sg.Frame('Tracks', trackTableLayout, vertical_alignment='top', pad=((0, 10), (0, 0))),
        sg.Frame('Items', itemTableLayout, vertical_alignment='top')],
]


def addNewProject():
    fname = rppFile.browseFile()
    print(fname[0])
    projectFile = rppFile.openFile(fname[0])
    rppFile.printStruct(projectFile)
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
    pnum = db.addProject(dtls)
    data.addProject(pnum, dtls)
    projectTable.update(data.projectTableData.values())

    tracks = projectFile.findall('TRACK')
    print('Project has %d tracks' % len(tracks))
    for tnum in range(0, len(tracks)):
        track = tracks[tnum]
        trackDtls = [track.find('NAME')[1], track.find('MAINSEND')[1], track.find('VOLPAN')[1], track.find('VOLPAN')[2],
                     ",".join([lst[1] for lst in track.findall('AUXRECV')])]
        tnotes = track.find('S&M_TRACKNOTES')
        if tnotes is not None:
            txt = "\n".join([tnotes[n][1:] for n in range(0, len(tnotes))])
        else:
            txt = ""
        trackDtls.append(txt)
        data.addTrack(pnum, tnum, trackDtls)
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
            data.addItem(pnum, tnum, inum, itemDtls)
            db.addItem([pnum, tnum, inum] + itemDtls)
        fxchain = track.find('FXCHAIN')
        if fxchain is not None:
            preset = None
            vst = None
            items = fxchain.find('.')
            for inum in range(0, len(items)):
                item = items[inum]
                if isinstance(item, list) and item[0] == 'PRESETNAME':
                    preset = item[1]
                    print('PRESETNAME=' + item[1] + ' goes with VST ' + str(vst))
                    pluginDtls = [vst[0], vst[1], item[1]]
                    data.addPlugin(pnum, tnum, inum, pluginDtls)
                    db.addPlugin([pnum, tnum, inum] + pluginDtls)
                    preset = None
                elif isinstance(item, rpp.element.Element):
                    if item.tag == 'VST':
                        vst = item.attrib[0:2]
                        print('VST=' + str(vst))


def createMyWindow():
    global window
    window = sg.Window("Windows-like program", layout, default_element_size=(12, 1),
                       auto_size_text=False, auto_size_buttons=False,
                       default_button_element_size=(12, 1),
                       finalize=True, resizable=True)
    window.Hide()


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


def showMyWindow():
    window.UnHide()

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        # ------ Process menu choices ------ #
        if event == 'About...':
            sg.popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...')
        elif event == 'Run Reaper':
            print(event)
        elif event == 'Add Project':
            addNewProject()
        elif event == 'Delete Project':
            print(event)
        elif event == 'Print Project':
            print(event)
        elif event == 'PROJECTS':
            print(values['PROJECTS'])
            row = values['PROJECTS'][0]
            pnum = sorted(data.projectTableData.keys())[row]
            window.find_element('location').update(chunkStr(data.projectTableData[pnum][3], 50)) # 50 is text width
            window.find_element('tempo').update(data.projectTableData[pnum][4])
            window.find_element('record_path').update(chunkStr(data.projectTableData[pnum][5], 50)) # 50 is text width
            window.find_element('sample_rate').update(data.projectTableData[pnum][6])
            window.find_element('project_notes').update(data.projectTableData[pnum][7])
            data.showTracks(trackTable, pnum)
            window.find_element('main_send').update('')
            window.find_element('vol').update('')
            window.find_element('pan').update('')
            window.find_element('aux_recvs').update('')
            window.find('file').update('')
            data.showItems(itemTable, -1, -1)
            data.showPlugins(pluginTable, -1, -1)
        elif event == 'TRACKS':
            print(values['TRACKS'])
            prow = values['PROJECTS'][0]
            pnum = sorted(data.projectTableData.keys())[prow]
            trow = values['TRACKS'][0]
            tnum = sorted(data.trackTableData[pnum].keys())[trow]
            window.find_element('main_send').update(data.trackTableData[pnum][tnum][1])
            window.find_element('vol').update(data.trackTableData[pnum][tnum][2])
            window.find_element('pan').update(data.trackTableData[pnum][tnum][3])
            ar = window.find_element('aux_recvs')
            mstr = chunk(data.trackTableData[pnum][tnum][4].split(","), 25) # 25 is width of aux_recvs
            ar.update(mstr)
            data.showItems(itemTable, pnum, tnum)
            data.showPlugins(pluginTable, pnum, tnum)
        elif event == 'ITEMS':
            print(values['ITEMS'])
            prow = values['PROJECTS'][0]
            pnum = sorted(data.projectTableData.keys())[prow]
            trow = values['TRACKS'][0]
            tnum = sorted(data.trackTableData[pnum].keys())[trow]
            irow = values['ITEMS'][0]
            inum = sorted(data.itemTableData[pnum][tnum].keys())[irow]
            window.find_element('file').update(chunkStr(data.itemTableData[pnum][tnum][inum][3], 50))
        else:
            print(event, values)
    window.close()
    db.close()


def showProjects(projectTableData):
     projectTable.update(projectTableData.values())
