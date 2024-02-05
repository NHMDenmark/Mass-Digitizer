# -*- coding: utf-8 -*-
"""
  Created on August 16, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: The home screen or starting point of the application, where the user is asked to choose institution and log in.  
"""

import PySimpleGUI as sg

# Internal dependencies
import util
import global_settings as gs
import models.collection as coll
import data_access
import specify_interface
import specimen_data_entry as sde

db = data_access.DataAccess(gs.databaseName)
sp = specify_interface.SpecifyInterface()

class HomeScreen():
    # Get version number to set into the homeScreen welcome menu.
    version = util.getVersionNumber()
    
    util.logger.debug(f'Starting Mass Digitizer App version {version}')

    def __init__(self):
        """
        Constructor initializing GUI elements after fetching available institutions 
        """

        self.institutions = util.convert_dbrow_list(db.getRowsOnFilters('institution',{'visible = ': 1}))
        
        header_font = ("Corbel, 17")
        header = [sg.Text(f"DaSSCo Mass Digitizer App - Version {self.version}", size=(58,1), font=header_font, justification='left')]

        separator_line = [sg.Text('_'  * 80)]

        btn_exit = [sg.Button("Exit", key='btnExit')]

        lblSelectInstitution = [sg.Text('Please choose your institution to proceed:')]
        lstSelectInstitution = [sg.Combo(list(self.institutions), readonly=True, enable_events=True, key='institution')]

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

        layout = [[[sg.Column(col_main, key='colMain', size=(580,128))]],
                [[sg.Column(col_next, key='colNext', size=(512,220), visible=False)],
                [sg.Column(col_side, key='colSide', size=(512,64))]], ]

        self.window = sg.Window('Start', layout, size=(640, 400))

        self.main()



    def main(self):
        """
        Main loop of execution responding to user input 
        """        

        while True:
            event, values = self.window.read()
            
            if event == sg.WIN_CLOSED or event == 'Bye!':
                break
            
            if event == 'institution':
                selected_institution = values['institution']
                institution = db.getRowsOnFilters('institution', {' name = ':'"%s"'%selected_institution},1)
                institution_id = institution[0]['id']
                institution_url = institution[0]['url']
                gs.baseURL = institution_url
                collections = util.convert_dbrow_list(db.getRowsOnFilters('collection', {' institutionid = ':'%s'%institution_id, 'visible = ': '1'}), True)
                self.window['lstSelectCollection'].update(values=collections)
                self.window['colNext'].update(visible=True)

            if event == 'lstSelectCollection':
                username = values['inpUsername']
                password = values['inpPassword']
                
                if username != '' and password != '':
                    # A username and password has been entered 
                    selected_collection = values['lstSelectCollection']

                    collection = db.getRowsOnFilters('collection', {'name = ':'"%s"'%selected_collection,'institutionid = ':'%s'%institution_id,})
                    
                    if len(collection) > 0:
                        collection_id = collection[0]['id']

                        if collection_id > 0:
                            gs.baseURL = institution_url
                            gs.csrfToken = sp.specifyLogin(username, password, collection[0]['spid'])

                            if gs.csrfToken != '': # TODO Check token format for extra security 
                                # Login was successfull

                                gs.userName = username
                                gs.collectionName = selected_collection
                                gs.collection = coll.Collection(collection_id)
                                gs.institutionId = institution_id
                                gs.institutionName = selected_institution 

                                # 1. Fetch SpecifyUser on username (/api/specify/specifyuser/?name=username)
                                user = sp.getSpecifyObjects('specifyuser', filters={"name":f"{username}"})[0]
                                gs.spUserId = user['id']
                                # 2. Fetch Agent on specifyuser primary key (/api/specify/agent/?specifyuser=n)
                                agent = sp.getSpecifyObjects('agent', filters={"specifyuser": gs.spUserId})[0]
                                # 3. Store full name in global settings (as single, concatenated string of first, middle, last)
                                gs.firstName = agent['firstname']
                                gs.middleInitial = agent['middleinitial']
                                gs.lastName = agent['lastname']

                                self.window.close()
                                
                                sde.SpecimenDataEntry(collection_id)
                            else:
                                self.window['autherror'].Update(visible=True)
                                self.window['lstSelectCollection'].update(set_to_index=0)
                        else:
                            self.window['collerror'].Update(visible=True)
                else:
                    self.window['incomplete'].Update(visible=True)
                    self.window['lstSelectCollection'].update(set_to_index=0)

            if event == 'btnExit':
                break
            
        self.window.close()