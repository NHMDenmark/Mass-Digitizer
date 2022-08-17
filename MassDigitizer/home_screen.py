from queue import Empty
import sys
import PySimpleGUI as sg

from pathlib import Path
sys.path.append(str(Path(__file__).joinpath('MassDigitizer')))

import data_access as db
import util

#window = Empty

header_font = ("Corbel, 18")
header = [sg.Text("Welcome to the DaSSCo Mass Digitizer App", size=(48,1), font=header_font, justification='center')]
separator_line = [sg.Text('_'  * 80)],

btn_exit = [sg.Button("Exit", key='exit')]

# Set up insitution selection field 
#institutions = ['NHMD: Natural History Museum of Denmark (Copenhagen)', 'NHMA: Natural History Museum Aarhus', 'TEST: Test server']
institutions = util.convert_dbrow_list(db.getRows('institution'))

lbl_select_institution = [sg.Text('Please choose your institution in order to proceed:')]
ddl_select_institution = [sg.Combo(list(institutions), readonly=True, enable_events=True, key='Institution')]

col_main = [ 
    header, 
    lbl_select_institution, 
    ddl_select_institution 
    ]

col_side = [
    btn_exit
    ]

layout = [ [sg.Column(col_main), sg.Column(col_side, element_justification='left')] ]

window = sg.Window('Start', layout, size=(640, 480))

def init():
    main(window)


def main(window):
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Bye!':
            break
        
        if event == 'Institution':
            
            selected_institution = values['Institution']
            
            print(event, selected_institution)

            

            next_col_main = [ 
                [sg.Text("Welcome to the DaSSCo Mass Digitizer App", size=(48,1), font=header_font, justification='center')],
                [sg.Text('You selected the following instutition:')], 
                [sg.Text(selected_institution)], 
                [sg.Text('Please choose a collection:')],
                [sg.Combo(list(institutions), readonly=True, enable_events=True, key='collection')]
                ]

            next_col_side = [
                #btn_exit
                ]

            next_layout = [ [sg.Column(next_col_main), sg.Column(next_col_side, element_justification='left')] ]

            next_window = sg.Window('Start', next_layout, size=(640, 480))
            window.close()
            window = next_window

        
    window.close()

init()