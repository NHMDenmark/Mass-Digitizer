from tkinter import CENTER, RIGHT
import PySimpleGUI as sg

headlineFont = ("Corbel, 18")

headline = [sg.Text("Welcome to the DaSSCo Mass Digitizer App", size=(48,1), font=headlineFont, justification='center')]
separator_line = [sg.Text('_'  * 80)],

# Set up insitution selection field 
institutions = ['NHMD: Natural History Museum of Denmark (Copenhagen)', 'NHMA: Natural History Museum Aarhus', 'TEST: Test server']
lbl_select_institution = [sg.Text('Please choose your institution in order to proceed:')]
ddl_select_institution = [lbl_select_institution, sg.OptionMenu(list(institutions), key='__INSTITUTION__')]

layout = [ [headline], [separator_line], [ddl_select_institution] ]

window = sg.Window('Start', layout, size=(600, 480))
#window.

def init():
    while True:
        event, values = window.read()



        if event == sg.WIN_CLOSED or event == 'Bye!':
            break
        
    window.close()

init()