# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:44:00 2022
@authors: Jan K. Legind, NHMD; Fedor A. Steeman NHMD
Copyright 2022 Natural History Museum of Denmark (NHMD)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.
- Pop up window for assisting digitizer staff in the data entry effort.
- Be mindful that the autoSuggestObject gets populated as we progress through the code.
"""

import PySimpleGUI as sg
from itertools import chain

# Internal Dependencies
import data_access
import global_settings as gs
from models import model
from models import collection as coll

db = data_access.DataAccess(gs.databaseName)

class AutoSuggest_popup():
    startQueryLimit = 3
    # rowDict = {}
    # No. of keystrokes before auto suggest function is triggered.
    candidateNamesList = []
    rowCandidates = []
    done = False
    defaultBoxText = ''

    def __init__(self, table_name, collection_id):
        """
        Initialize
        """

        self.tableName = table_name
        self.collectionID = collection_id
        self.collection = coll.Collection(collection_id) #db.getRowOnId('collection', collection_id)
        print(self.collection)

        self.window = self.buildGui()

    def buildGui(self): #, customSQL='', colName=None, alternativeInputTitle= None):
        """ 
        Builds the interface for taxon name lookup as well as for novel names.
        """

        # dimensions of the popup list-box
        input_width = 95
        lines_to_show = 7
        titleText = ''
        highTaxText = 'Unknown taxon name. Specify parent.'
        # if alternativeInputTitle:
        #     titleText = alternativeInputTitle
        # defText = self.defaultBoxText

        layout = [
            [sg.Text('Input name:'+'initial', key="lblInputName", metadata='initial-name')],
             # sg.Text(labelText,
             #         key='lblNewName', visible=False, background_color='Turquoise3', metadata='invisible')],

            [sg.Input(default_text=self.defaultBoxText,  size=(input_width, 1), enable_events=True, key='txtInput'),
             sg.Button('OK', key='btnReturn', visible=False, bind_return_key=True),
             sg.Button('Exit', visible=False)
             # 'btnReturn' is for binding return to nothing in case of a new name and higher taxonomy lacking.
            ],
            [sg.Text('Input higher taxonomy:', key='lblHiTax', visible=False),
             sg.Input(size=(input_width, 1), enable_events=True, key='txtHiTax', visible=False)],
            [sg.pin(
                sg.Col([[sg.Listbox(values=[], size=(input_width, lines_to_show), enable_events=True, key='lstSuggestions',
                                    bind_return_key=True, select_mode='extended')]],
                       key='lstSuggestionsContainer', pad=(0, 0), visible=True))], ]

        window = sg.Window('Auto Complete', layout, return_keyboard_events=True, finalize=True, modal=False,
                           font=('Arial', 12), size=(810, 200))
        # The parameter "modal" is explicitly set to False. If True the auto close behavior won't work.

        self.lstSuggestionsElement: sg.Listbox = window.Element('lstSuggestions')  # store listbox element for easier access and to get to docstrings
        self.txtInput: sg.Text = window.Element('txtInput')
        
        window['txtHiTax'].bind('<FocusIn>', '+INPUT FOCUS+')
        window.Finalize = True # Needed for being able to reactivate window, otherwise PySimpleGUI will throw an error 
        window.hide()

        return window

    def captureSuggestion(self, keyStrokes, minimumCharacters=3):
        """
        TODO Explain function  
        Parameter keyStrokes is the 'name' as it is being inputted, keystroke-by-keystroke
        minimumCharacters is an integer on how many key strokes it takes to start the auto-suggester.
        """ 

        # Resetting base variables (TODO Explain variables)
        choices = [' ']
        prediction_list, input_text, sel_item = choices, "", 0
       
        # Using 'Model' base object (superclass) to encompass both derived models be it Storage or TaxonName
        autoSuggestObject = model.Model(self.collectionID)
        autoSuggestObject.table = self.tableName

        # Get GUI input events 
        window = self.window
        window['txtInput'].update(keyStrokes)
        window.write_event_value('txtInput', keyStrokes) # Adds event trigger for key strokes

        # GUI Event Loop
        while True:  
            # As long as the loop isn't exited somehow, continue checking events 
            event, values = window.read()
            print(event, values)
            
            # Escape loop & close window when exiting or otherwise done 
            if self.done: break
            if event is None: break
            if event == sg.WIN_CLOSED or event == 'Exit': break
            if event.startswith('Escape'): break
            
            # TODO comment 
            elif event.startswith('Down') and len(self.candidateNamesList):
                # TODO comment 
                sel_item = (sel_item + 1) % len(self.candidateNamesList)
                self.lstSuggestionsElement.update(set_to_index=sel_item, scroll_to_index=sel_item)

            elif event.startswith('Up') and len(self.candidateNamesList):
                # TODO comment 
                sel_item = (sel_item + (len(self.candidateNamesList) - 1)) % len(self.candidateNamesList)
                self.lstSuggestionsElement.update(set_to_index=sel_item, scroll_to_index=sel_item)

            if event.endswith('+TAB'):
                # TODO comment 
                #break
                pass
            
            if event == 'txtInput':
                # this concerns all keystrokes except the above ones.

                novelName = ''

                # When capture of suggestion has been marked as done, escape loop which will hide window

                
                # Get text input as keystrokes converted to lower case 
                keystrokes = values['txtInput'].lower()
                print(f"KEYSTROKKKKES: {keystrokes}")
                # TODO unclear what the following line are supposed to accomplish 
                #if keystrokes == input_text: continue
                #else: input_text = keystrokes
                if values['txtInput']:
                    print(f"getting hit with {values['txtInput']}")
                
                # Minimum number of keystroke characters (default: 3) should be met in order to proceed 
                if len(keystrokes) >= minimumCharacters:
                    # Fetch suggestions from database based on keystrokes 
                    suggestions = self.lookupSuggestions(keystrokes)
                    #fields = {'fullname' : f'LIKE lower("%{keyStrokes}%")', 'collectionid' : f'= {self.collection.id}'}

                    # Convert records to list of fullnames 
                    self.candidateNamesList = [row['fullname'] for row in suggestions]

                    if len(self.candidateNamesList) == 0:
                        pass
                    # Adjusts the listbox behavior to what is expected.
                    self.lstSuggestionsElement.update(values=self.candidateNamesList, set_to_index=[0])

                    # Focus back to text input field, to enable user to continue typing 
                    self.window['txtInput'].set_focus()

                # TODO comment
                #sel_item = 0
                print('LENGTH candidatename list ==: ', len(self.candidateNamesList))
                if len(self.candidateNamesList) > 1:
                    print('pred list more than NONE """', len(self.candidateNamesList))
                    # window['lblNewName'].update(visible=False)
                    window['lblHiTax'].update(visible=False)
                    window['txtHiTax'].update(visible=False)
                    window['btnReturn'].BindReturnKey = True
                    window['lstSuggestionsContainer'].update(visible=True)
                elif len(keystrokes) >= minimumCharacters and len(self.candidateNamesList) == 0:
                    print('Ccandidate list: ', len(self.candidateNamesList), " this is going to be a new name!!!")
                    window['lblInputName'].update('Please finish typing the new taxon name:')
                    # window['lblNewName'].update('!', visible=True)
                    window['lblInputName'].metadata = 'higherTaxon_name'
                    print(f"New taxon name string: {values['txtInput']}")

                    # if len(self.candidateNamesList) == 0:
                    #     window[event].update(value='')
                    #     # prediction_list.append(' ')

            # TODO commment
            if event == 'lstSuggestions' or event == 'btnReturn':
                print('Selected suggestion : ', type(values['lstSuggestions']), values['lstSuggestions'])
                print('Selected parent     : ', values['txtInput'])
                ##Trigger txtInput !!!!!!!


                if len(values['lstSuggestions']) > 0:
                    # A known name is selected (?)
                    boxVal = values['lstSuggestions']
                    if self.tableName == 'storage':
                        column = 'name'
                    else:
                        column = 'fullname'

                    atomicNames = boxVal[0].split('|')
                    atomic = atomicNames.pop()
                    atomic = atomic.strip()

                    selected_row = next(row for row in suggestions if row[column]==atomic)
                    selected_row = dict(selected_row)
                    print("selected_row ", selected_row)
                    
                    # TODO comment 
                    autoSuggestObject.table = self.tableName
                    autoSuggestObject.id = selected_row['id']
                    autoSuggestObject.spid = selected_row['spid']
                    autoSuggestObject.name = selected_row['name']
                    autoSuggestObject.fullName = selected_row['fullname']
                    autoSuggestObject.collectionId  = self.collectionID
                    autoSuggestObject.parentFullName = selected_row['parentfullname']
                    
                    # TODO comment
                    novelName = selected_row['name']
                                        
                    if window['lblInputName'].metadata == 'higherTaxon_name':
                        # TODO Check to see if we are in the 'Add higher taxonomy section'
                        # Parent name is set to the taxon name selected.
                        window['lblInputName'].update('Please finish typing the HIGHER TAXON name:')
                        window['txtInput'].update('')
                        autoSuggestObject.parentFullName = selected_row['name']

                    # TODO done ? 
                    break
                else:
                    
                    # A new name is assumed and user is asked to input higher taxon name 

                    #if window['lblInputName'].metadata != 'higherTaxon-name':
                    if self.tableName == 'taxonname':

                        # TODO comment : Make autosuggest for higher taxonomy available again.
                        autoSuggestObject.table = self.tableName
                        autoSuggestObject.name = window['txtInput'].split(' ').pop()
                        autoSuggestObject.fullName = window['txtInput']
                        autoSuggestObject.collectionId  = self.collectionID
                        autoSuggestObject.parentFullName = '' 

                        #novelName = sg.popup_get_text('Unknown taxon name. Press OK when finished.', default_text=keystrokes, modal=True)
                        #print("The NEW NAME is : ", novelName)
                        autoSuggestObject.name = window
                        window['lblInputName'].metadata = 'higherTaxon-name'
                        window['lblInputName'].update('Please input higher taxonomy:')
                        # Setting the metadata label so that ELSE: can be reached.

                    else:
                        autoSuggestObject.parentFullName = novelName
                        hiTaxName = window['txtInput'].get()

                        newHigherTaxonName = sg.popup_get_text('Please finish typing the higher taxon name:',
                                                                default_text=hiTaxName)
                        autoSuggestObject.parentFullName = newHigherTaxonName
                        print(f"model parentfullname={autoSuggestObject.parentFullName}, "
                                f"name={autoSuggestObject.name}")
                        #return autoSuggestObject
                        break
                            
                        # novelNameModel = model.Model(self.collectionID)


                    print('NEW higher taxon name ', values['txtHiTax'])
                    return values['txtHiTax']

        # TODO If new taxon name then save ! 

        if window is not None: 
            try:
                window.Hide()
            except: 
                print('Window may have been closed manually')

        print(autoSuggestObject)

        return autoSuggestObject

    def lookupSuggestions(self, keyStrokes, columnName='fullname', customSQL='', taxDefItemId=None, rowLimit=200):
        """ 
        Database lookup of suggestions based on three or more entered characters. 
         keyStrokes: This parameter is the supplied keyStrokes from the user.
         rowLimit: at or below this the auto-suggest fires of its names
         returns: a list of names
         TODO implement 'taxonTreeDefid' at convienient time.
        """
        responseType = ''
        # Local variable to determine the auto-suggest type: 'storage', taxon-keyStrokes, or 'parent taxon-name'.
        # It is included in the return statement.

        # TODO Question: Why not use the db.getRows method ???
        cur = db.getDbCursor()
        sql = f"SELECT * FROM {self.tableName} WHERE {columnName} LIKE lower('%{keyStrokes}%');"

        # TODO Explain function of below lines 
        if taxDefItemId:
            sql = sql[:-1]
            sql = sql + ' AND taxontreedefid = {};'.format(taxDefItemId)
        elif customSQL:
            sql = customSQL
        
        rows = cur.execute(sql).fetchall()

        return rows

    def Show(self):
        """Make auto-suggest popup window visible""" 

        # If window has been forcefully closed rebuild
        if self.window is None: self.window = self.buildGui

        # Make window visible 
        self.window.UnHide()

    def Hide(self):
        """Make auto-suggest popup window invvisible""" 
        
        # If window has been forcefully closed rebuild 
        if self.window is None: self.window = self.buildGui
        
        # Make window visible 
        self.window.Hide()

    def flatten_rows(self, rowsObject):
        flatCandidates = list(chain.from_iterable(rowsObject))
        rows = list(flatCandidates)
        print('length flattened rows ::: ', len(rows))
        return rows

    def __exit__(self, exc_type, exc_value, traceback):
        print("\nInside __exit__")



# EXE section -- remember "taxonname" or "storage"#
# ob = AutoSuggest_popup('taxonname', 29)
# autoTaxonName = ob.Show()
# ob.autosuggest_gui('')
# ob.autoSuggest_popup.AutoSuggest_popup('taxonname', 29)

