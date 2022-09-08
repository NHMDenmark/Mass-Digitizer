import sys
import PySimpleGUI as sg

from pathlib import Path
sys.path.append(str(Path(__file__).joinpath('MassDigitizer')))

import util
import global_settings as gs
import data_access as db
import specimen_data_entry as de
import specify_interface as sp


def init():
    # TODO function contract 

    header_font = ("Corbel, 18")
    header = [sg.Text("DaSSCo Mass Digitizer App", size=(32,1), font=header_font, justification='center')]
    separator_line = [sg.Text('_'  * 80)]

    btn_exit = [sg.Button("Exit", key='exit')]

    # Set up insitution selection field 
    #institutions = ['NHMD: Natural History Museum of Denmark (Copenhagen)', 'NHMA: Natural History Museum Aarhus', 'TEST: Test server']
    institutions = util.convert_dbrow_list(db.getRows('institution'))

    lblSelectInstitution = [sg.Text('Please choose your institution to proceed:')]
    lstSelectInstitution = [sg.Combo(list(institutions), readonly=True, enable_events=True, key='institution')]

    lblSelectCollection = [sg.Text('Choose a collection to log in:', key='lblSelectCollection')]
    lstSelectCollection = [sg.Combo({'-select a collection-'}, key='lstSelectCollection', readonly=True, size=(28, 1), enable_events=True)]

    col_main = [header, separator_line, lblSelectInstitution, lstSelectInstitution, ]

    col_next = [[sg.Text('Enter your Specify username & password and then choose collection.')],
                [sg.Text('Specify username:')], 
                [sg.InputText(size=(24,1), background_color='white', text_color='black', key='inpUsername')],
                [sg.Text('Specify password:')], 
                [sg.InputText(size=(24,1), background_color='white', text_color='black', key='inpPassword', password_char='*')],
                lblSelectCollection, lstSelectCollection, 
                [sg.Text('Please fill in username/password!', text_color='red', visible=False, key='incomplete')], 
                [sg.Text('Authentication Error!', text_color='red', visible=False, key='autherror')], 
                [sg.Text('Please choose a collection!', text_color='red', visible=False, key='collerror')], ]

    col_side = [btn_exit]

    layout = [[[sg.Column(col_main, key='colMain', size=(480,128))]],
            [[sg.Column(col_next, key='colNext', size=(480,200), visible=False)],
            [sg.Column(col_side, key='colSide', size=(480,64))]], ]

    window = sg.Window('Start', layout, size=(480, 400))

    main(window)

def main(window):
    # Run main loop waiting for input 
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Bye!':
            break
        
        if event == 'institution':
            selected_institution = values['institution']
            institution = db.getRowsOnFilters('institution', {' name = ':'"%s"'%selected_institution})
            institution_id = institution[0]['id']
            institution_url = institution[0]['url']
            collections = util.convert_dbrow_list(db.getRowsOnFilters('collection', {' institutionid = ':'%s'%institution_id, 'visible = ': '1'}), True)

            window['lstSelectCollection'].update(values=collections)
            window['colNext'].update(visible=True)

        if event == 'lstSelectCollection':
            username = values['inpUsername']
            password = values['inpPassword']
            
            if username != '' and password != '':

                selected_collection = values['lstSelectCollection']
                collection = db.getRowsOnFilters('collection', {
                                                'name = ':'"%s"'%selected_collection, 
                                                'institutionid = ':'%s'%institution_id,})
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
                            #window['lstSelectCollection'].set_value([])
                            pass
                    else:
                        window['collerror'].Update(visible=True)
            else:
                window['incomplete'].Update(visible=True)
                #window['lstSelectCollection'].set_value([])
                pass
        
    window.close()

#init()