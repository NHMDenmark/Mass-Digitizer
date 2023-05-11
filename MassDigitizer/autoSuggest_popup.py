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

# Internal Dependencies
import util 
import data_access
import global_settings as gs

from models import model
from models import collection as coll

class AutoSuggest_popup():
    '''
    Generic Autosuggest class catering to taxon names, and storage for now.
    '''
    classFamily = ''
    taxonName = ''
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
        self.currentRecord = None # Retrievable specimen record
        self.novelTaxon = False

        # Using 'Model' base object (superclass) to encompass both derived models be it Storage or TaxonName
        self.autoSuggestObject = None # Set to None as it should be re-instantiated at every capture 

        self.suggestions = []
        self.selected_row = None


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
        self.autoSuggestObject = model.Model(self.collectionID) #%specimen.Specimen(self.collectionID)
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
            
            # Handle up or down arrow press in family suggestion box
            # Down arrow is pressed: Move selection down
            if event.startswith('Down') and len(self.candidateNamesList) > 0: 
                # When you arrow down and there are candidate names in the list, set new selected item: 
                select_item = (select_item + 1) % len(self.candidateNamesList) # Increase selected item index within length of candidate name list 
                self.select_item_index = select_item # Set class variable value of the selected item index 
                self.lstSuggestionsElement.update(values=self.candidateNamesList, set_to_index=select_item, scroll_to_index=select_item) # select item in listbox and focus on it 
            # Up arrow is pressed: Move selection up
            elif event.startswith('Up') and len(self.candidateNamesList): 
                # When you arrow up and there are candidate names in the list, set new selected item: 
                select_item = (select_item + (len(self.candidateNamesList) - 1)) % len(self.candidateNamesList) # Decrease selected item index within length of candidate name list 
                self.select_item_index = select_item # Set class variable value of the selected item index 
                self.lstSuggestionsElement.update(values=self.candidateNamesList, set_to_index=select_item, scroll_to_index=select_item)
            
            # If keystrokes are entered in the taxon name input box 
            elif event == 'txtInput':
                # Get text input as keystrokes converted to lower case 
                keystrokes = values['txtInput'].lower()
                
                # Minimum number of keystroke characters (default: 3) should be met in order to proceed 
                if int(len(keystrokes)) >= int(minimumCharacters):
                    # Filter suggestion list based on keystrokes 
                    self.handleSuggestions(keystrokes, 'rankid', '=')
                    # Focus back to text input field, to enable user to continue typing 
                    self.window['txtInput'].set_focus()
            
            elif event == 'txtHiTax':
                # Family name is being entered: Update suggestions with family names
                # This input field is only visible in case of an unknown taxon 
                higherTaxonName = values['txtHiTax']
                self.autoSuggestObject.familyName = higherTaxonName
                if len(higherTaxonName) >= minimumCharacters:
                    self.handleSuggestions(values['txtHiTax'].lower(), 140, '=') # Rank Family is assumed (rank id: 140)

                # If a suggestion is clicked in the listbox OR 'Enter' is pressed then handle suggested taxon name
                # TODO| this is a mess of 'if' statements and should be simplified. There must be a split between
                # TODO| the section dealing with novel names and the known name case.
                taxonFullName = values['txtInput']
                self.autoSuggestObject.taxonFullName = taxonFullName
                taxonName = taxonFullName.split(' ')[-1]
                self.autoSuggestObject.taxonName = taxonName
                window['frmHiTax'].update(visible=True)


            elif event == 'lstSuggestions' or event == 'btnReturn':
                # If there still are entries in the list box then this is a known name and the one selected is handled 
                if len(values['lstSuggestions']) > 0:
                    # As long as there are suggestions available: A known name is selected 
                    selectedSuggestion = values['lstSuggestions'][0]

                    # Iterate suggestion list until selection is hit 
                    self.selected_row = next(row for row in self.suggestions if row['fullname']==selectedSuggestion)
                    self.selected_row = dict(self.selected_row)

                    # Prepare autosuggest object 
                    self.autoSuggestObject.table         = self.tableName
                    self.autoSuggestObject.collectionId  = self.collectionID

                    if self.tableName == 'taxonname':

                        # Populate the object as taxon name 

                        self.rankId = self.selected_row['rankid']
                        self.autoSuggestObject.rankid = self.rankId 
                        self.autoSuggestObject.treedefid = self.collection.taxonTreeDefId
                        self.familyName = self.searchParentTaxon(self.selected_row['fullname'], 140, self.collection.taxonTreeDefId)
                        self.autoSuggestObject.familyName = self.familyName
                        self.currentRecord = self.autoSuggestObject.getFieldsAsDict()
                        # The above family name will be picked up by the specimen-data-entry class

                    if self.tableName == 'storage': #STORAGE
                        # Populate the object as storage location
                        self.autoSuggestObject.name     = self.selected_row['name']
                        self.autoSuggestObject.fullName = self.selected_row['fullname']
                        self.autoSuggestObject.rankName = self.selected_row['rankname']

                    # If text input box for higher taxon is not available then a known taxon is selected 
                    if window['frmHiTax'].visible == False:

                        # Set taxon name fields for return and escape since no higher taxon is necessary.
                        # self.autoSuggestObject.rankid   = selected_row['rankid']
                        self.autoSuggestObject.id       = self.selected_row['id']
                        self.autoSuggestObject.spid     = self.selected_row['spid']
                        self.autoSuggestObject.name     = self.selected_row['name']
                        self.autoSuggestObject.fullName = self.selected_row['fullname']
                        self.autoSuggestObject.parentFullName = self.selected_row['parentfullname']
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
                    if self.tableName == 'taxonname':
                        # Unknown taxon: Switch to family name search
                        window['frmHiTax'].update(visible=True) # Reveal family name input fields 
                        window['txtHiTax'].SetFocus() # Set focus on family name text input 
                        
                        # Store novel taxon name in autosuggest object 
                        self.autoSuggestObject.name = values['txtInput'].strip().split(' ').pop()
                        self.autoSuggestObject.fullName = values['txtInput'].strip()

                        if values['lstSuggestions']:  # Asking for family name.
                            self.autoSuggestObject.parentFullName = values['lstSuggestions'][0]
                        else: # family name submitted not recognized or empty.
                            self.autoSuggestObject.parentFullName = values['txtHiTax']
                        self.autoSuggestObject.familyName = self.searchParentTaxon(self.autoSuggestObject.parentFullName, 140, self.collection.taxonTreeDefId)
                        self.familyName = self.autoSuggestObject.familyName
                window['txtHiTax'].update(self.familyName)

                # elif self.novelTaxon:
                #     # Since the listbox is empty a NOVEL! name has been set to True
                #     if self.tableName == 'taxonname':
                #
                #         # New taxon name is assumed and higher taxon input field is made available
                #         window['frmHiTax'].update(visible=True)
                #         window['txtHiTax'].SetFocus()
                #         self.autoSuggestObject.id       = 0
                #         self.autoSuggestObject.spid     = 0
                #         self.autoSuggestObject.name     = values['txtInput'].split(' ').pop()
                #         self.autoSuggestObject.fullName = values['txtInput']
                #
                #         if values['lstSuggestions']: # Asking for family name.
                #             self.autoSuggestObject.parentFullName = values['lstSuggestions'][0]
                #         else:
                #             self.autoSuggestObject.parentFullName = values['txtHiTax']
                #             self.autoSuggestObject.higherTaxonName = None
                #             # self.autoSuggestObject.parentFullName = values['lstSuggestions'][0] #selected_row['parentfullname']
                #         self.autoSuggestObject.familyName = self.searchParentTaxon(self.autoSuggestObject.parentFullName, 140, self.collection.taxonTreeDefId)
                #         self.familyName = self.autoSuggestObject.familyName

            elif event == 'btnOK' :
                # Approval of family selected for novel taxon entry 
                # 
                self.classFamily = self.familyName.strip() # TODO explain 
                self.taxonName = self.autoSuggestObject.name.strip()
                self.autoSuggestObject.familyName = self.familyName.strip()
                
                self.autoSuggestObject.table = self.tableName
                self.autoSuggestObject.id   = 0
                self.autoSuggestObject.spid = 0
                # self.autoSuggestObject.name = values['txtInput'].split(' ').pop()
                # self.autoSuggestObject.name = values['txtInput']
                # self.autoSuggestObject.fullName = f"{self.autoSuggestObject.name}".strip(' ')
                self.autoSuggestObject.collectionId  = self.collectionID
                self.autoSuggestObject.notes =  f" Verbatim_taxon:{self.autoSuggestObject.fullName}"
                self.autoSuggestObject.parentFullName = values['txtHiTax'].strip()
                self.autoSuggestObject.familyName = values['txtHiTax'].strip()
                self.autoSuggestObject.rankid = self.determineRank(self.autoSuggestObject.fullName)

                # TODO Persist novel taxon so it will be auto-suggested next time around
                self.db.insertRow('taxonname', {"name": f'"{self.autoSuggestObject.name.strip()}"', 
                                                "fullname": f'"{self.autoSuggestObject.fullName.strip()}"',
                                                "rankid": f'{self.autoSuggestObject.rankid}',
                                                "parentfullname": f'"{self.autoSuggestObject.parentFullName}"',
                                                "treedefid": f'{self.collection.taxonTreeDefId}',
                                                "taxonrank": f'"{self.autoSuggestObject.rankName}"',
                                                } )

                window['frmHiTax'].update(visible=False) # Hide family search panel for next taxon name entry 
                break

        if window is not None: 
            # Escaped event loop: Try to close window 
            try:
                window.Hide()
            except:
                util.logger.error('Attempt to close autosuggest window failed...')
                
        return self.autoSuggestObject

    def determineRank(self, taxonNameEntry):
        """
        Determine rank of given taxon name entry  
        TODO Function contract 
        """
        rankid = 999
        try: 
            elementCount = len(taxonNameEntry.strip().split(' '))
            subgenusCount = 0
            if '(' in taxonNameEntry: subgenusCount = 1

            if ' var. ' in taxonNameEntry: rankid = 240
            elif ' subvar.  ' in taxonNameEntry: rankid = 250
            elif ' f. ' in taxonNameEntry: rankid = 260 
            elif ' subf. ' in taxonNameEntry: rankid = 270 
            elif elementCount == 3 + subgenusCount: rankid = 230
            elif elementCount == 2 + subgenusCount: rankid = 220
            elif elementCount == 1 + subgenusCount: rankid = 180
        except: 
            util.logger.error(f'Could not determine rank of novel taxon: {taxonNameEntry}')
        
        return rankid

    def handleSuggestions(self, keyStrokes, rankId=270, rankSign='<='):  # rank id 270 == 'subforma'
        """
        Fetch suggestions from database based on keystrokes 
        TODO Function contract 
        """

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
            #self.novelTaxon = True

        # Adjusts the listbox behavior to what is expected.
        #self.lstSuggestionsElement.update(values=self.candidateNamesList, set_to_index=[0])
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

    def searchParentTaxon(self, taxonName, target_rankid, treedefid):
        """
        Will traverse a given taxon's parental lineage until it hits the target rank 
        taxonName: is the desired name to acquire a family name for.
        target_rankid: is the target rank
        returns: target higher rank concept
        """
        
        taxonRankId = 270 # Start with lowest possible rank

        # Keep on traversing parental branch until the specified rank level has been passed
        while (taxonRankId >= target_rankid):
            # Get current taxon record on fullname and taxon tree   
            taxonNameRecords = self.db.getRowsOnFilters('taxonname', filters={'fullname': f"='{taxonName}'", 'treedefid': f"= '{treedefid}'"})

            if len(taxonNameRecords) > 0: 
                taxonRankId = taxonNameRecords[0]['rankid']
                taxonName = taxonNameRecords[0]['name']
                parentName = taxonNameRecords[0]['parentfullname'] # TODO More secure with primary keys 
                
                # Return when given taxon already matches rank or is of higher rank
<<<<<<< HEAD
                if taxonRankId < target_rankid:
                    # self.taxonName = ''
                    break
=======
                if taxonRankId <= target_rankid:
                    return taxonName
>>>>>>> 8d9f2806927df54982cf3b77c7102cca680f3ee9
                else:
                    # Target rank not yet hit; check next parent in line 
                    return (self.searchParentTaxon(parentName, target_rankid, treedefid))
                
            else:
                # Can't find (further) parent taxon 
                #taxonName = '-not found-'  
                #raise Exception(f"Could not retrieve parent taxon of target rank: {target_rankid} !") 
                break # return current
        
        return taxonName
    
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

    def get_name(self):

        return self.taxonName

    def __exit__(self, exc_type, exc_value, traceback):
        pass
