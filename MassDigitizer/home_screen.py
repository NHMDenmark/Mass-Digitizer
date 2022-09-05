import sys
import PySimpleGUI as sg

from pathlib import Path
sys.path.append(str(Path(__file__).joinpath('MassDigitizer')))

import util
import global_settings as gs
import data_access as db
import specimen_data_entry as de
import specify_interface as sp

#window = Empty

header_font = ("Corbel, 18")
header = [sg.Text("Welcome to the DaSSCo Mass Digitizer App", size=(48,1), font=header_font, justification='center')]
separator_line = [sg.Text('_'  * 80)],

btn_exit = [sg.Button("Exit", key='exit')]

# Set up insitution selection field 
#institutions = ['NHMD: Natural History Museum of Denmark (Copenhagen)', 'NHMA: Natural History Museum Aarhus', 'TEST: Test server']
institutions = util.convert_dbrow_list(db.getRows('institution'))

lbl_select_institution = [sg.Text('Please choose your institution in order to proceed:')]
ddl_select_institution = [sg.Combo(list(institutions), readonly=True, enable_events=True, key='institution')]

col_main = [ 
    header, 
    lbl_select_institution, 
    ddl_select_institution, 
    [sg.Text('Authentication Error!', text_color='red', visible=False)], 
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
        
        if event == 'institution':
            
            selected_institution = values['institution']
            #selected_institution_id = keys['']
            #print(event, selected_institution)
            institution = db.getRowsOnFilters('institution', {' name = ':'"%s"'%selected_institution})
            institution_id = institution[0]['id']
            institution_url = institution[0]['url']
            collections = util.convert_dbrow_list(db.getRowsOnFilters('collection', {' institutionid = ':'%s'%institution_id, 'visible = ': '1'}), True)

            next_col_main = [ 
                [sg.Text("Welcome to the DaSSCo Mass Digitizer App", size=(48,1), font=header_font, justification='center')],
                [sg.Text('You selected the following instutition:')], 
                [sg.Text(selected_institution), ], 
                [sg.Text('Specify username:')], 
                [sg.InputText(size=(24,1), background_color='white', text_color='black', key='username')],
                [sg.Text('Specify password:')], 
                [sg.InputText(size=(24,1), background_color='white', text_color='black', key='password', password_char='*')],
                [sg.Text('Choose a collection to log in:')],
                [sg.Combo(list(collections), readonly=True, enable_events=True, key='collection')],
                [sg.Text('Please fill in username/password!', text_color='red', visible=False, key='incomplete')], 
                [sg.Text('Authentication Error!', text_color='red', visible=False, key='autherror')], 
                [sg.Text('Please choose a collection!', text_color='red', visible=False, key='collerror')], 
                ]

            next_col_side = [
                #btn_exit
                ]

            next_layout = [ [sg.Column(next_col_main), sg.Column(next_col_side, element_justification='left')] ]

            next_window = sg.Window('Start', next_layout, size=(640, 480))
            window.disappear()
            window = next_window

        if event == 'collection':
            username = values['username']
            password = values['password']
            print(username,password)

            if username != '' and password != '':

                selected_collection = values['collection']
                collection = db.getRowsOnFilters('collection', {
                                                'name = ':'"%s"'%selected_collection, 
                                                'institutionid = ':'%s'%institution_id,
                                                })
                if len(collection) > 0:
                    collection_id = collection[0]['id']

                    if collection_id > 0:
                        gs.baseURL = institution_url
                        gs.csrfToken = sp.specifyLogin(username, password, collection_id)

                        if gs.csrfToken != '':
                            gs.spUserName = username
                            gs.collectionId = collection_id
                            gs.collectionName = selected_collection
                            gs.institutionId = institution_id
                            gs.institutionName = selected_institution
                            window.close()
                            de.init(collection_id)
                        else:
                            window['autherror'].Update(visible=True)
                            #window['collection'].set_value([])
                            pass
                    else:
                        window['collerror'].Update(visible=True)
            else:
                window['incomplete'].Update(visible=True)
                #window['collection'].set_value([])
                pass
        
    window.close()

#init()