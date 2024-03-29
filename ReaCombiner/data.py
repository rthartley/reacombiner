import os
import string

import PySimpleGUI as sg
from fpdf import FPDF

from ReaCombiner import file_utils
from ReaCombiner.file_utils import errorMsg


class MyPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'in', 'Letter')
        from tkinter import font
        import tkinter
        root = tkinter.Tk()
        fonts = list(font.families())
        fonts.sort()
        root.destroy()

        self.fontName = 'Arial'
        self.fontStyle = ''
        self.fontSize = 12
        self.set_xy(0.0, 0.0)

    def adjustWidth(self, str: str, width: float, slice: int):
        if slice > 0 and self.get_string_width(str[0:-slice]) > width or slice == 0 and self.get_string_width(
                str) > width:
            return self.adjustWidth(str, width, slice + 3)
        else:
            return slice

    def setFont(self, name: string = None, style=None, size=None):
        if name is not None:
            self.fontName = name
        if style is not None:
            self.fontStyle = style
        if size is not None:
            self.fontSize = size
        self.set_font(self.fontName, self.fontStyle, self.fontSize)

    def writeStr(self, str: string, width: float, height: float, align: str = 'L', ln=1,
                 setx=None, color=None, name=None, size=None, style=None, border=0, extras=None):
        if extras is None:
            extras = []
        self.setFont(name, style, size)
        if color is not None:
            self.set_text_color(*color)
        slice = self.adjustWidth(str, width, 0)
        if slice == 0:
            self.cell(w=width, h=height, align=align,
                      txt=str.encode(encoding='ascii', errors='backslashreplace').decode(),
                      border=border, ln=ln)
            return extras
        else:
            str1 = str[0:-slice]
            setx = self.get_x()
            self.cell(w=width, h=height, align=align,
                      txt=str1.encode(encoding='ascii', errors='backslashreplace').decode(),
                      border=border, ln=ln)
            return self.getExtras(str[-slice:], setx, width, height, align, border, extras, 0)

    def writeExtras(self, extras):
        for line in extras:
            i = len(line)
            for str in line:
                props = line[str]
                self.set_x(props["x"])
                self.cell(w=props["width"], h=props["height"],
                          txt=str.encode(encoding='ascii', errors='backslashreplace').decode(),
                          ln=1 if i == 1 else 0)
                i -= 1

    def getExtras(self, str, x, width, height, align, border, extras, i):
        lex = len(extras)
        slice = self.adjustWidth(str, width, 0)
        if slice == 0:
            if i < lex:
                extras[i][str] = {"x": x, "width": width, "height": height}
            else:
                extras.append({str: {"x": x, "width": width, "height": height}})
            return extras
        else:
            str1 = str[0:-slice]
            if i < lex:
                extras[i][str1] = {"x": x, "width": width, "height": height}
            else:
                extras.append({str1: {"x": x, "width": width, "height": height}})
            str2 = str[-slice:]
            return self.getExtras(str2, x, width, height, align, border, extras, i + 1)


pluginTypes = ['VST', 'VSTi', 'VST3', 'JS', 'REWIRE']


class Plugin:
    def __init__(self, pluginNum: int, name: str, file: str, preset: str):
        self.pluginNum = pluginNum
        self.name = name
        self.file = file
        self.preset = preset

    def getPluginDetails(self):
        return [self.name, self.file, self.preset]

    def print(self, pdf: FPDF, dh: float, indent: float):
        pdf.writeStr(self.name, 4.5, dh, setx=indent, ln=0)
        pdf.writeStr(self.file, 1.75, dh, ln=0)
        pdf.writeStr("None" if self.preset == '' else self.preset, 2.0, dh)


class Item:
    def __init__(self, itemNum: int, name: str, source: str, position: str, file: str):
        self.itemNum = itemNum
        self.name = name
        self.source = source
        self.position = position
        self.file = file

    def getItemDetails(self):
        return [self.name, self.source, self.position]

    def print(self, pdf: MyPDF, dh: float, indent: float):
        extras1 = pdf.writeStr(self.name, 2.0, dh, setx=indent, ln=0)
        pdf.writeStr(self.source, 0.5, dh, ln=0)
        pdf.writeStr(str(self.position), 1.5, dh, ln=0)
        extras = pdf.writeStr(self.file, 2.0, dh, extras=extras1)
        if len(extras) > 0:
            pdf.writeExtras(extras)


class Track:
    def __init__(self, trackNum: int, name: str, mainSend: str, vol: str, pan: str, auxReceives: str, trackNotes: str):
        self.name = name
        self.trackNum = trackNum
        self.mainSend = mainSend
        self.vol = vol
        self.pan = pan
        self.auxReceives = auxReceives
        self.sends = []
        self.items = {}
        self.plugins = {}
        self.trackNotes = trackNotes

    def addSend(self, num: int):
        self.sends.append(num)

    def addItem(self, item: Item):
        self.items[item.itemNum] = item

    def addPlugin(self, plugin: Plugin):
        self.plugins[plugin.pluginNum] = plugin

    def getTrackDetails(self):
        return [self.trackNum, self.name]

    def getItems(self):
        return self.items

    def getPlugins(self):
        return self.plugins

    def print(self, pdf: MyPDF, dh: float, indent: float):
        pdf.writeStr('Track %d: %s' % (self.trackNum, self.name), 2.0, 0.3, style='B', size=12)
        pdf.writeStr('Main send', 1.0, dh, setx=indent, size=10, ln=0)
        pdf.writeStr('Vol', 1.5, dh, ln=0)
        pdf.writeStr('Pan', 1.5, dh, ln=0)
        pdf.writeStr('Aux Receives', 2.3, dh, ln=0)
        pdf.writeStr('Sends', 1.5, dh)
        pdf.writeStr('Yes' if self.mainSend == '1' else 'No', 1.0, height=dh, setx=indent, style='', ln=0)
        pdf.writeStr(self.vol, 1.5, dh, ln=0)
        pdf.writeStr(self.pan, 1.5, dh, ln=0)
        extras = pdf.writeStr("None" if self.auxReceives == '' else self.auxReceives, width=2.3, height=dh, ln=0)
        pdf.writeStr('None' if len(self.sends) == 0 else ','.join(self.sends), 1.5, dh)
        if len(extras) > 0:
          pdf.writeExtras(extras)
        if len(self.trackNotes) > 0:
            pdf.writeStr('Notes', 1.0, dh, setx=indent)
            pdf.writeStr(self.trackNotes, 2.0, 3.0, align='T', setx=indent)
        items = self.items.values()
        if len(items) > 0:
            pdf.writeStr('Item Name', 2.0, dh, setx=indent, size=10, style='B', ln=0)
            pdf.writeStr('Source', 0.5, dh, ln=0)
            pdf.writeStr('Position', 1.5, dh, ln=0)
            pdf.writeStr('File', 2.0, dh)
            pdf.setFont(size=10, style='')
            for item in items:
                item.print(pdf, dh, indent)
        plugins = self.plugins.values()
        if len(plugins) > 0:
            pdf.writeStr('Plugin Name', 4.5, dh, setx=indent, style='B', size=10, ln=0)
            pdf.writeStr('File', 1.75, dh, ln=0)
            pdf.writeStr('Preset', 2.0, dh)
            pdf.setFont(style='', size=10)
            for plugin in plugins:
                plugin.print(pdf, dh, indent)


class Project:
    def __init__(self, projectNum: int, name: str, mix: str, date: str, location: str,
                 tempo: str, recordPath: str, sampleRate: str, projectNotes: str):
        self.projectNum = projectNum
        self.name = name
        self.mix = mix
        self.date = date
        self.location = location
        self.recordPath = recordPath
        self.tempo = tempo
        self.sampleRate = sampleRate
        self.projectNotes = projectNotes
        self.tracks = {}

    def addTrack(self, track: Track):
        self.tracks[track.trackNum] = track

    def getTrack(self, trackNum: int):
        return self.tracks[trackNum]

    def getTracks(self):
        return self.tracks

    def getProjectDetails(self):
        return [self.name, self.mix, self.date]

    def printPlugins(self, pdf: MyPDF, dh: float):
        pdf.writeStr('Plugins:', 3.5, dh)
        pluginNames = {}
        for track in self.tracks.values():
            tp = track.getPlugins()
            for pl in tp.values():
                name = pl.name
                if name not in pluginNames:
                    pluginNames[name] = 1
                else:
                    pluginNames[name] = pluginNames[name] + 1
        for pn, n in pluginNames.items():
            pdf.writeStr(pn if n == 1 else pn + ' (%s)' % str(n), 6.5, dh, setx=0.6)

    def print(self):
        pdf = MyPDF()
        pdf.add_page()
        dh = 0.2
        indent = 0.6
        pdf.writeStr(self.name, 7.5, 0.5, align='C', color=(220, 50, 50), size=18)
        pdf.writeStr('Mix %s on %s' % (self.mix, self.date), 7.5, 0.5, align='C', size=14)
        pdf.writeStr('Location: %s' % self.location, 3.5, dh, color=(0, 0, 0), size=10, style='B')
        pdf.writeStr('Tempo: %s' % self.tempo, 3.5, dh)
        pdf.writeStr('Sample Rate: %s' % self.sampleRate, 3.5, dh)
        pdf.writeStr('Tracks: %d' % len(self.tracks), 3.5, dh)
        self.printPlugins(pdf, dh)
        if len(self.projectNotes) > 0:
            pdf.writeStr('Notes', 1.0, dh, size=12)
            pdf.setFont(size=10, style='')
            for note in self.projectNotes.split('\n'):
                pdf.writeStr(note, 7.0, dh, setx=indent)
        pdf.ln(0.15)
        pdf.line(pdf.get_x(), pdf.get_y(), 8.5 - pdf.get_x(), pdf.get_y())
        pdf.ln(0.15)
        for track in self.tracks.values():
            track.print(pdf, dh, indent)
            f = ''
        f = file_utils.browseDir('Destination')
        if f == '':
            return
        try:
            path = f + '/%s.pdf' % self.name
            if os.path.exists(path):
                ans = sg.popup_ok_cancel("File exists. Are you absolutely sure?")
                if 'Cancel' == ans:
                    return
            pdf.output(path, 'F')
            file_utils.lastBrowseDir = f
            sg.popup_ok('Printing finished to ' + path)
        except (PermissionError, RuntimeError):
            errorMsg('Could not write to file')


class Projects:
    def __init__(self):
        self.projects = []  # a list by row number
        self.maxProjectNum = 0

    def addProject(self, project: Project):
        self.projects.append(project)

    def getProject(self, rowNum: int):
        return self.projects[rowNum]

    def getProjects(self):
        return self.projects

    def setProjects(self, projects):
        self.projects = projects

    def findProjectNum(self, projectNum: int):
        for project in self.projects:
            if project.projectNum == projectNum:
                return project
        return None

    def findProject(self, project: Project):
        dtls = project.getProjectDetails()
        for p in self.projects:
            pdtls = p.getProjectDetails()
            if dtls == pdtls:
                # we already have the project
                return "_EXISTS_"
            elif dtls[0:2] == pdtls[0:2]:
                # it's the same mix but  a different date, so delete
                # the project and reinsert it
                return p
        return None

    def deleteProject(self, pnum: int):
        for p in self.projects:
            if p.projectNum == pnum:
                self.projects.remove(p)
                return

    def updateProjects(self, projects):
        self.projects = sorted(projects, key=lambda proj: proj.name.upper())

    def sortProjects(self, sortBy, upordown):
        self.projects = sorted(self.projects, key=sortBy, reverse=upordown)


allProjects: Projects = Projects()


def newShowTracks(table, project: Project = None):
    if project is None:
        table.update([])
    else:
        tracks = project.getTracks()
        table.update([track.getTrackDetails() for track in tracks.values()])


def newShowItems(table, track: Track = None):
    if track is None:
        table.update([])
    else:
        table.update([item.getItemDetails() for item in track.getItems().values()])


def newShowPlugins(table, track: Track = None):
    if track is None:
        table.update([])
    else:
        table.update([plugin.getPluginDetails() for plugin in track.getPlugins().values()])
