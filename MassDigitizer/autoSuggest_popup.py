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
import util 
import data_access
import global_settings as gs
from models import model
from models import collection as coll
from models import specimen


class AutoSuggest_popup():
    '''
    Generic Autosuggest class catering to taxon names, and storage for now.
    '''
    classFamily = ''
    def __init__(self, table_name, collection_id):
        """
        Initialize
        """

        #self.startQueryLimit = 3 # No. of keystrokes before auto suggest function is triggered
        self.candidateNamesList = [] # list/array of candidate names 
        self.select_item_index = 0   # index of selected item i.e. position in list box
    
        self.db = data_access.DataAccess(gs.databaseName) 
        self.tableName = table_name
        self.collectionID = collection_id
        self.collection = coll.Collection(collection_id)
        self.familyName = '' # Global var to capture the family-name from searchParentTaxon()
        self.rankId = 0 # global var for taxon rank id.

        # Using 'Model' base object (superclass) to encompass both derived models be it Storage or TaxonName
        self.autoSuggestObject = None # Set to None as it should be re-instantiated at every capture 

        self.suggestions = []

        self.window = self.buildGui()

    def buildGui(self):
        """ 
        Builds the interface for taxon name lookup as well as for novel names.
        """

        # dimensions of the popup list-box
        input_width = 95
        lines_to_show = 7

        layout = [
            [sg.Text('Input name:', key="lblInputName", metadata='initial-name')],
             # sg.Text(labelText,
             #         key='lblNewName', visible=False, background_color='Turquoise3', metadata='invisible')],

            [sg.Input(default_text='', key='txtInput', size=(input_width, 1), enable_events=True),
             sg.Button('OK', key='btnReturn', visible=False, bind_return_key=True),
             sg.Button('Exit', visible=False)
             # 'btnReturn' is for binding return to nothing in case of a new name and higher taxonomy lacking.
            ],
            [sg.Frame('New taxon name detected...', [
            [sg.Text('Input family name:', key='lblHiTax'),
             sg.Input(size=(24, 1), key='txtHiTax', enable_events=True), 
             sg.Button('OK', key='btnOK')]], #button OK is used to submit the novel name.
             key='frmHiTax', expand_x=True, visible=False)],
            [sg.pin(
                sg.Col([[sg.Listbox(values=[], key='lstSuggestions', size=(input_width, lines_to_show), enable_events=True,
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
        Parameter keyStrokes is the 'name' as it is being inputted, keystroke-by-keystroke
        minimumCharacters is an integer on how many key strokes it takes to start the auto-suggester.
        """ 

        # Re-instantiate blank autoSuggest object
        self.autoSuggestObject = specimen.Specimen(self.collectionID)
        self.autoSuggestObject.table = self.tableName

        # Resetting base variables 
        select_item = 0 # index of selected item i.e. the position in the listbox 
       
        # Get GUI input events 
        window = self.window
        window['txtInput'].update(keyStrokes)
        window.write_event_value('txtInput', keyStrokes) # Adds event trigger for key strokes

        # GUI Event Loop
        while True:  
            # As long as the loop isn't somehow exited , then continue checking events
            event, values = window.read()

            # Escape loop & close window when exiting or otherwise done 
            if event is None: break
            if event == sg.WIN_CLOSED or event == 'Exit': break
            if event.startswith('Escape'): break           
            
            # Listbox element is unfortunately not born with up/down arrow capability.
            if event.startswith('Down') and len(self.candidateNamesList) > 0:
                # When you arrow down and there are candidate names in the list, set new selected item: 
                select_item = (select_item + 1) % len(self.candidateNamesList) # Increase selected item index within length of candidate name list 
                self.select_item_index = select_item # Set class variable value of the selected item index 
                self.lstSuggestionsElement.update(values=self.candidateNamesList, set_to_index=select_item, scroll_to_index=select_item) # select item in listbox and focus on it 

            elif event.startswith('Up') and len(self.candidateNamesList):
                # Listbox element is not born with up/down arrow capability.
                select_item = (select_item + (len(self.candidateNamesList) - 1)) % len(self.candidateNamesList) # Decrease selected item index within length of candidate name list 
                self.select_item_index = select_item # Set class variable value of the selected item index 
                self.lstSuggestionsElement.update(values=self.candidateNamesList, set_to_index=select_item, scroll_to_index=select_item)
            
            # If keystrokes are entered in the taxon name input box 
            elif event == 'txtInput':
                # Get text input as keystrokes converted to lower case 
                keystrokes = values['txtInput'].lower()
                
                # Minimum number of keystroke characters (default: 3) should be met in order to proceed 
                if int(len(keystrokes)) >= int(minimumCharacters):
                    self.handleSuggestions(keystrokes, 'rankid', '=')
                    # Focus back to text input field, to enable user to continue typing 
                    self.window['txtInput'].set_focus()
                                               
            elif event == 'txtHiTax':
                # Family name taxon is being entered: Update suggestions
                higherTaxonName = values['txtHiTax'] # Family name
                self.autoSuggestObject.familyName = higherTaxonName
                if len(higherTaxonName) >= minimumCharacters:
                    self.handleSuggestions(values['txtHiTax'].lower(), 140, '=') # Rank Family is assumed (rank id: 140)

            # If a suggestion is clicked in the listbox OR 'Enter' is pressed then handle suggested taxon name 
            elif event == 'lstSuggestions' or event == 'btnReturn':
                #Fix for novel parent name

                # If there still are entries in the list box then this is a known name and the one selected is handled 
                if len(values['lstSuggestions']) > 0:
                    # A known name is selected 
                    selectedSuggestion = values['lstSuggestions'][0]

                    # Iterate suggestion list until selection is hit 
                    selected_row = next(row for row in self.suggestions if row['fullname']==selectedSuggestion)
                    selected_row = dict(selected_row)

                    # TODO comment below 
                    self.autoSuggestObject.table         = self.tableName
                    self.autoSuggestObject.collectionId  = self.collectionID

                    if self.tableName == 'taxonname':

                        rankID = selected_row['rankid']

                        self.rankId = rankID
                        self.autoSuggestObject.treedefid = self.collection.taxonTreeDefId
                        self.autoSuggestObject.rankid    = 999 # Generic catchall rank id
                        self.familyName = self.searchParentTaxon(selected_row['fullname'], 140,
                                                                            self.collection.taxonTreeDefId)
                        self.autoSuggestObject.familyName = self.familyName
                        # The above family name will be picked up by the specimen-data-entry class

                    if self.tableName == 'storage': #STORAGE

                        # Populate the object as storage
                        self.autoSuggestObject.name     = selected_row['name']
                        self.autoSuggestObject.fullName = selected_row['fullname']
                        self.autoSuggestObject.rankName = selected_row['rankname']

                    # If text input box for higher taxon is not available then a known taxon is selected 
                    if window['frmHiTax'].visible == False:

                        # Set taxon name fields for return and escape since no higher taxon is necessary.
                        # self.autoSuggestObject.rankid   = selected_row['rankid']
                        self.autoSuggestObject.id       = selected_row['id']
                        self.autoSuggestObject.spid     = selected_row['spid']
                        self.autoSuggestObject.name     = selected_row['name']
                        self.autoSuggestObject.fullName = selected_row['fullname']
                        self.autoSuggestObject.parentFullName = selected_row['parentfullname']
                        break                     
                    else:

                        # Inputting novel taxon name
                        # self.autoSuggestObject.rankid = selected_row['rankid']
                        self.autoSuggestObject.rankid = 0

                        # if not self.autoSuggestObject.parentFullName:

                        window['txtHiTax'].Update(self.autoSuggestObject.parentFullName)
                        #window['frmHiTax'].update(visible=False)
                        window['btnOK'].SetFocus()                        
                        
                        #self.autoSuggestObject.save()                   
                    #break # Stay for confirmation of higher taxon entry
                else:                    
                    # Since the listbox is empty a new name is assumed 
                    if self.tableName == 'taxonname':
                        # New taxon name is assumed and higher taxon input field is made available
                        window['frmHiTax'].update(visible=True)
                        window['txtHiTax'].SetFocus()
                        self.autoSuggestObject.id       = 0
                        self.autoSuggestObject.spid     = 0
                        self.autoSuggestObject.name     = values['txtInput'].split(' ').pop()
                        self.autoSuggestObject.fullName = values['txtInput']

                        if values['lstSuggestions']:
                            self.autoSuggestObject.parentFullName = values['lstSuggestions'][0]
                        else:
                            self.autoSuggestObject.parentFullName = values['txtHiTax']
                            self.autoSuggestObject.higherTaxonName = None
                            # self.autoSuggestObject.parentFullName = values['lstSuggestions'][0] #selected_row['parentfullname']
                        self.autoSuggestObject.familyName = self.searchParentTaxon(self.autoSuggestObject.parentFullName, 140, self.collection.taxonTreeDefId)
                        self.familyName = self.autoSuggestObject.familyName

            elif event == 'btnOK' :

                self.classFamily = self.familyName
                self.autoSuggestObject.familyName = self.familyName
                # OK button pressed during new taxon entry
                self.tableName = 'specimen' # Added as temporary patch due to incompatible columns.
                # Will need an update to handle novel taxon name entries into table taxonname.
                self.autoSuggestObject.table = self.tableName
                self.autoSuggestObject.id   = 0
                self.autoSuggestObject.spid = 0
                # self.autoSuggestObject.name = values['txtInput'].split(' ').pop()
                self.autoSuggestObject.name = values['txtInput']
                self.autoSuggestObject.fullName = f"{self.autoSuggestObject.name}".strip(' ')
                self.autoSuggestObject.collectionId  = self.collectionID
                taxonomic_comment = f" Verbatim_taxon:{self.autoSuggestObject.fullName}"
                self.autoSuggestObject.notes = taxonomic_comment
                self.autoSuggestObject.parentFullName = values['txtHiTax']
                self.autoSuggestObject.familyName = values['txtHiTax']
                self.autoSuggestObject.rankid = 999
                window['frmHiTax'].update(visible=False)
                break

        if window is not None: 
            # Escaped event loop: Try to close window 
            try:
                window.Hide()
            except:
                util.logger.error('Attempt to close autosuggest window failed...')
        return self.autoSuggestObject

    def handleSuggestions(self, keyStrokes, rankId=270, rankSign='<='):  # rank id 270 == 'subforma'
        # Fetch suggestions from database based on keystrokes 
        #self.suggestions = self.lookupSuggestions(keystrokes, 'fullname', minimumRank)

        try:
            if self.tableName == 'storage':
                fields = {'name' : f'LIKE lower("%{keyStrokes}%")', 'collectionid' : f'= {self.collection.collectionId}' }
                self.suggestions = data_access.DataAccess(gs.databaseName).getRowsOnFilters('storage', fields, 200)

            else: # taxon
                self.tableName = 'taxonname'
                fields = {'fullname': f'LIKE lower("%{keyStrokes}%")',
                          'treedefid': f'= {self.collection.taxonTreeDefId}', 'rankid': f'{rankSign}{rankId}'}
                self.suggestions = data_access.DataAccess(gs.databaseName).getRowsOnFilters('taxonname', fields, 200)

        except Exception as e:
            util.logger.error(e)
            sg.PopupError(e)

        # Convert records to list of fullnames 
        self.candidateNamesList = [row['fullname'] for row in self.suggestions]

        if self.select_item_index:
            if self.select_item_index >= 0:
                self.lstSuggestionsElement.update(values=self.candidateNamesList, set_to_index=self.select_item_index, scroll_to_index=self.select_item_index) # select item in listbox and focus on it 
        else:
            self.lstSuggestionsElement.update(values=self.candidateNamesList, set_to_index=0, scroll_to_index=0)
        # Adjusts the listbox behavior to what is expected.
        # self.lstSuggestionsElement.update(values=self.candidateNamesList, set_to_index=[0])
        return self.candidateNamesList

    # def lookupSuggestions(self, keyStrokes, columnName='fullname', minimumRank=270, rowLimit=200):
    #     """
    #     Database lookup of suggestions based on three or more entered characters.
    #      keyStrokes: This parameter is the supplied keyStrokes from the user.
    #      rowLimit: at or below this the auto-suggest fires of its names
    #      returns: a list of SQLite rows
    #      TODO implement 'treeDefid' at convienient time.
    #     """
    #     responseType = ''
    #     # Local variable to determine the auto-suggest type: 'storage', taxon-keyStrokes, or 'parent taxon-name'.
    #     # It is included in the return statement.
    #
    #     # Get candidate name list from db based on keystrokes, rank and taxon tree
    #     filters = {columnName       : f"LIKE lower('%{keyStrokes}%')",
    #                'treedefid' : f"{self.collection.taxonTreeDefId}",
    #                'rankid'         : f"rankid <= {minimumRank}"
    #                }
    #     rows = self.db.getRowsOnFilters(self.tableName, filters, rowLimit)
    #
    #     return rows

    def searchParentTaxon(self, taxonName, rankid, treedefid):
        ''' Will climb the taxonname table to get at the family name which is rankid 140
       taxonName: is the desired name to acquire a family name for.
       rankid: is the target rank , in this case 'family' - id = 140
       returns: target higher rank concept
    '''
        while (taxonName != rankid):  # The logic for this while() makes no sense but serves its purpose to keep going.
            # taxonRankID = 0
            try:
                taxonName = f"= '{taxonName}'"
                treedefid_format = f"= '{treedefid}'"
                spTaxon = self.db.getRowsOnFilters('taxonname', filters={'fullname': taxonName, 'treedefid': treedefid_format})

                # for j in spTaxon:
                #     print('spTaxon row:', [k for k in j]) # Sanity check for family search
                # print('len(spTaxon)', len(spTaxon), spTaxon[0])
                if len(spTaxon) > 0:
                    taxonRankId = spTaxon[0][4]
                    taxonId = spTaxon[0][0]
                    taxonName = spTaxon[0][3]
                    parentName = spTaxon[0][6]

                    if taxonRankId == rankid:
                        return taxonName
                    elif taxonRankId < 140:
                        # return 'unknown'
                        return ''
                    else:
                        return (self.searchParentTaxon(parentName, rankid, treedefid))
                else:
                    return 0
            except:
                return ''
    def Show(self):
        """Make auto-suggest popup window visible""" 

        # If window has been forcefully closed rebuild
        #if self.window is None: 
        self.window = self.buildGui()

        # Make window visible 
        self.window.UnHide()

    def Hide(self):
        """Make auto-suggest popup window invvisible""" 
        
        # If window has been forcefully closed rebuild 
        if self.window is None: self.window = self.buildGui
        
        # Make window visible 
        self.window.Hide()

    def flatten_rows(self, rowsObject):
        # The SQLite rowsObject is slightly odd in that it is a "list of dicts", but not really.
        flatCandidates = list(chain.from_iterable(rowsObject))
        rows = list(flatCandidates)
        return rows

    def get_family(self):
        return self.classFamily

    def __exit__(self, exc_type, exc_value, traceback):
        pass



# EXE section -- remember "taxonname" or "storage"#
# ob = AutoSuggest_popup('taxonname', 29)
# autoTaxonName = ob.Show()
# ob.autosuggest_gui('')
# ob.autoSuggest_popup.AutoSuggest_popup('taxonname', 29)

