import PySimpleGUI as sg

sg.ChangeLookAndFeel('LightGreen')
sg.SetOptions(element_padding=(0, 0))

# ------ Menu Definition ------ #
menu_def = [['File', ['Add Project', 'DeleteProject', 'Print Project', 'Exit']],
            ['Run', ['Run Reaper']],
            ['Help', 'About...'], ]

projectTableHeadings = ['Project', 'Take', 'Last Modified']
projectTableHeader = [[sg.Text(h, size=(15, 1)) for h in projectTableHeadings]]
projectTableInputRows = [[sg.Input(size=(15, 1), pad=(0, 0)) for col in range(3)] for row in range(10)]
projectTexts = [[sg.Text('Location', justification='r', pad=((0, 10), (15, 5))), sg.InputText(size=(25, 1), pad=((0, 0), (15, 5)))],
                [sg.Text('Tempo', justification='r', pad=((0, 10), (0, 5))), sg.InputText(size=(25, 1), pad=((0, 0),(0, 5)))],
                [sg.Text('Record Path', justification='r', pad=((0, 10), (0, 0))), sg.InputText(size=(25, 1), pad=((0, 0),(0, 5)))],
                [sg.Text('Sample Rate', justification='r', pad=((0, 10), (0, 0))), sg.InputText(size=(25, 1), pad=((0, 0),(0, 5)))],
                [sg.Frame("Project Notes", [[sg.Multiline(size=(40, 10))]], pad=((0, 0), (15, 15)))]]
projectTableLayout = projectTableHeader + projectTableInputRows + projectTexts


trackTableHeadings = ['Number', 'Track Name']
trackTableHeader = [[sg.Text(h, size=(15, 1)) for h in trackTableHeadings]]
trackTableInputRows = [[sg.Input(size=(15, 1), pad=(0, 0)) for col in range(2)] for row in range(10)]
trackTexts = [[sg.Text('Main Send', justification='r', pad=((0, 10), (15, 5))), sg.InputText(size=(25, 1), pad=((0, 0), (15, 5)))],
                [sg.Text('Vol', justification='r', pad=((0, 10), (0, 5))), sg.InputText(size=(25, 1), pad=((0, 0), (0, 5)))],
                [sg.Text('Pan', justification='r', pad=((0, 10), (0, 5))), sg.InputText(size=(25, 1), pad=((0, 0), (0, 5)))],
                [sg.Text('Aux Recvs', justification='r', pad=((0, 10), (0, 5))), sg.InputText(size=(25, 1), pad=((0, 0), (0, 5)))],
                [sg.Frame("Track Notes", [[sg.Multiline(size=(40, 10))]], pad=((0, 0), (15, 15)))]]
trackTableLayout = trackTableHeader + trackTableInputRows + trackTexts

itemTableHeadings = ['Item Name', 'Source', 'Position']
itemTableHeader = [[sg.Text(h, size=(15, 1)) for h in itemTableHeadings]]
itemTableInputRows = [[sg.Input(size=(15, 1), pad=(0, 0)) for col in range(3)] for row in range(10)]
pluginTableHeadings = ['Name', 'File', 'Preset']
pluginTableHeader = [[sg.Text(h, size=(15, 1)) for h in pluginTableHeadings]]
pluginTableInputRows = [[sg.Input(size=(15, 1), pad=(0, 0)) for col in range(3)] for row in range(10)]

itemTexts = [[sg.Text('File', justification='r', pad=((0, 0), (15, 0))), sg.InputText(size=(32, 1), pad=((0, 0), (15, 0)))],
             [sg.Frame('Plugins', pluginTableHeader + pluginTableInputRows, pad=(10,10))]]
itemTableLayout = itemTableHeader + itemTableInputRows + itemTexts

# ------ GUI Defintion ------ #
layout = [
    [sg.Menu(menu_def, )],
    [sg.Frame('Projects', projectTableLayout, pad=((0, 10), (0, 0))),
     sg.Frame('Tracks', trackTableLayout, pad=((0, 10), (0, 0))),
     sg.Frame('Items', itemTableLayout, vertical_alignment='top')],
]


def showMyWindow():
    window = sg.Window("Windows-like program", layout, default_element_size=(12, 1),
                       auto_size_text=False, auto_size_buttons=False,
                       default_button_element_size=(12, 1))

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        print('Button = ', event)
        # ------ Process menu choices ------ #
        if event == 'About...':
            sg.popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...')
        elif event == 'Run Reaper':
            print(event)
        elif event == 'Add Project':
            print(event)
        elif event == 'Delete Project':
            print(event)
        elif event == 'Print Project':
            print(event)
        else:
            pass
    window.close()
