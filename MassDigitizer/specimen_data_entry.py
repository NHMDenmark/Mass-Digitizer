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
"""

import PySimpleGUI as sg
import sys

# Internal dependencies
import util
from data_access import DataAccess
import global_settings as gs
import data_exporter as dx
import autoSuggest_popup
from models import specimen
from models import recordset

class SpecimenDataEntry():
    """
    Interface for entering specimen records.  
    """

    def __init__(self, collection_id):
        """
        Constructor that initializes class variables and dependent class instances 
        """
        util.logger.info("Initializing Data Entry form for Institution & collection: %s | %s" % (gs.institutionName, gs.collectionName))
        
        self.collectionId = collection_id  # Set collection Id
        self.window = None  # Create class level instance of window object
        self.db = DataAccess(gs.databaseName)  # Instantiate database access module
        self.collobj = specimen.Specimen(collection_id)  # Create blank specimen record instance
        self.recordSet = recordset.RecordSet(collection_id, 3) # Create recordset of last 3 saved records 
        
        # Various lists of fields to be cleared on command 
        self.focusIconList   = ['iconStorage','iconPrepType','iconTypeStatus','iconNotes','iconMultiSpecimen','iconGeoRegion','iconTaxonName','iconCatalogNumber']
        self.clearingList    = ['inpStorage', 'txtStorageFullname', 'cbxPrepType', 'cbxTypeStatus', 'txtNotes','chkMultiSpecimen', 
                                'cbxGeoRegion', 'inpTaxonName', 'txtCatalogNumber', 'txtRecordID','txtMultiSpecimen']
        self.stickyFields    = [{'txtStorageFullname'}, {'cbxPrepType'}, {'cbxTypeStatus'}, {'txtNotes'},
                                {'chkMultiSpecimen'}, {'txtMultiSpecimen'}, {'cbxGeoRegion'}, {'inpTaxonName'}]
        self.nonStickyFields = ['txtCatalogNumber', 'txtRecordID']

        # Global variables 
        self.notes = '' # Notes for access in autoSuggest_popup 
        self.fieldInFocus = '' # Stores name of field currently in focus 
        
        # Create auto-suggest popup windows
        self.autoStorage = autoSuggest_popup.AutoSuggest_popup('storage', collection_id)     #  for storage locations
        self.autoTaxonName = autoSuggest_popup.AutoSuggest_popup('taxonname', collection_id) # for taxon names
        
        # Set up user interface 
        self.setup(collection_id)
        
        # Run 
        self.main()

    def setup(self, collection_id):
        """
        Initialize data entry form on basis of collection id
        """
        util.logger.info('*** Specimen data entry setup ***')

        # Define UI areas
        sg.theme('SystemDefault')
        greenArea = '#E8F4EA'  # Stable fields   (?)
        blueArea  = '#99ccff'  # Variable fields (?)
        greyArea  = '#BFD1DF'  # Session & Settings

        # Set standard element dimensions
        captionSize     = (22, 1)  # Ensure element labels (captions) are the same size so that they line up
        greenSize       = (21, 1)  # Default width of all fields in the 'green area'
        blueSize        = (35, 1)  # Default width of all fields in the 'blue area'
        sessionInfoSize = (14, 1)

        # Set text fonts
        titleFont       = ('Bahnschrift', 18)
        captionFont     = ('Bahnschrift', 13)
        fieldFont       = ('Arial', 12) #
        sessionInfoFont = ('Bahnschrift', 12)
        smallLabelFont  = ('Arial', 11, 'italic')
        wingdingFont    = ('Wingding', 16)

        # Set special characters 
        indicatorRight = '◀'
        indicatorLeft = '▶'
        self.highlight = '#fffbef'

        # NOTE Elements are stored  in variables to make it easier to include and position in the frames

        # Green Area elements
        storage = [
            sg.Text("Storage location:", size=(21, 1), background_color=greenArea, font=captionFont),
            sg.Text(indicatorLeft, key='linStorage', text_color=greenArea, background_color=greenArea, visible=True, font=wingdingFont),
            sg.InputText('None', key='inpStorage', focus=True, size=greenSize, text_color='black', pad=(10,0), background_color='white', font=fieldFont, enable_events=True),
            sg.Text(indicatorRight, key='iconStorage', background_color=greenArea, visible=True, font=wingdingFont),
            sg.Text("", key='txtStorageFullname', size=(50, 2), background_color=greenArea, font=smallLabelFont)
            ]
        
        preparation = [
            sg.Text("Preparation type:", size=captionSize, justification='l', background_color=greenArea, font=captionFont),
            sg.Text(indicatorLeft, key='linPreptype', text_color=greenArea, background_color=greenArea, visible=True, font=wingdingFont),
            sg.Combo(util.convert_dbrow_list(self.collobj.prepTypes), key='cbxPrepType', size=greenSize, text_color='black', background_color='white', font=fieldFont, readonly=True, enable_events=True, pad=(0,0)),
            sg.Text(indicatorRight, key='iconPrepType', background_color=greenArea, visible=False, font=wingdingFont)
            ]

        type_status = [
            sg.Text('Type status:', size=captionSize, background_color=greenArea, font=captionFont),
            sg.Text(indicatorLeft, key='linTypeStatus', text_color=greenArea, background_color=greenArea, visible=True, font=wingdingFont),
            sg.Combo(util.convert_dbrow_list(self.collobj.typeStatuses), key='cbxTypeStatus', size=greenSize, text_color='black', background_color='white', font=fieldFont, readonly=True, enable_events=True, pad=(0,0)),
            sg.Text(indicatorRight, pad=(7,0), key='iconTypeStatus', background_color=greenArea, visible=False, font=wingdingFont ),
            ]
        
        notes = [
            sg.Text('Notes', size=captionSize, background_color=greenArea, font=captionFont),
            sg.Text(indicatorLeft, key='linNotes', text_color=greenArea, background_color=greenArea, visible=True, font=wingdingFont),
            sg.InputText(size=(80,5), key='txtNotes', pad=(0,0), enable_events=False, font=fieldFont, background_color='white', text_color='black'),
            sg.Text(indicatorRight, key='iconNotes', background_color=greenArea, visible=False, font=wingdingFont)
            ]

        multispecimen = [
            sg.Checkbox('Multispecimen object', key='chkMultiSpecimen', size=(20, 1), enable_events=True, font=captionFont, background_color=greenArea), 
            sg.InputText(size=(80,5), key='txtMultiSpecimen', background_color='white', text_color='black', pad=(3, 0), enable_events=True, font=fieldFont, visible=False), 
            sg.Text(indicatorRight, key='iconMultiSpecimen', background_color=greenArea, visible=False, font=wingdingFont)
            ]

        layout_greenarea = [storage, preparation, type_status, notes, multispecimen, ]

        # Blue Area elements
        broadGeo = [
            sg.Text('Broad geographic region:', size=captionSize, background_color=blueArea, text_color='black', font=captionFont),
            sg.Text(indicatorLeft, key='linGeoRegion', text_color=blueArea, background_color=blueArea, visible=True, font=wingdingFont),
            sg.Combo(util.convert_dbrow_list(self.collobj.geoRegions), size=blueSize, key='cbxGeoRegion', text_color='black', background_color='white', font=fieldFont, readonly=True, enable_events=True),
            sg.Text(indicatorRight, key='iconGeoRegion', background_color=blueArea, visible=False, font=wingdingFont)
            ]
        
        taxonInput = [
            sg.Text('Taxonomic name:     ', size=captionSize, background_color=blueArea, text_color='black', font=captionFont),
            sg.Text(indicatorLeft, key='linTaxonName', text_color=blueArea, background_color=blueArea, visible=True, font=wingdingFont),
            sg.Input('', size=blueSize, key='inpTaxonName', text_color='black', background_color='white', font=fieldFont, enable_events=True, pad=((5, 0), (0, 0))),
            sg.Text(indicatorRight, key='iconTaxonName', background_color=blueArea, visible=True, font=wingdingFont),
            sg.Text('No further record to go back to!', key='lblRecordEnd', visible=False, background_color="#ff5588", border_width=3)
            ]

        barcode = [
            sg.Text('Barcode:', size=captionSize, background_color=blueArea, enable_events=True, text_color='black', font=captionFont),
            sg.Text(indicatorLeft, key='linCatalogNumber', text_color=blueArea, background_color=blueArea, visible=True, font=wingdingFont),
            sg.InputText('', key='txtCatalogNumber', size=blueSize, text_color='black', background_color='white', font=fieldFont, enable_events=True), 
            sg.Text(indicatorRight, key='iconCatalogNumber', background_color=blueArea, visible=False, font=wingdingFont),
            ]

        # statusLabel = [sg.Text('Specimen record has been saved', font=('Arial',20),size=(20,10),justification='center',background_color='#4f280a',text_color= 'yellow',key='texto')]

        self.headers = ['id', 'spid',  'catalognumber',   'multispecimen', 'taxonfullname',  'taxonname',    'taxonnameid',
                        'taxonspid',   'highertaxonname', 'preptypename',  'typestatusname', 'typestatusid', 'georegionname', 
                        'georegionid', 'storagefullname', 'storagename']
        self.tableHeaders = ['id', 'catalognumber', 'taxonfullname', 'multispecimen', 'georegionname', 'storagename', 'notes'] # Headers for previousRecordsTable

        lblExport = [sg.Text('', key='lblExport', visible=False, size=(100, 2)), ]

        lblExport = [sg.Text('', key='lblExport', visible=False, size=(100, 2)), ]
        adjacentRecords = self.recordSet.getAdjacentRecordList(self.tableHeaders)
        previousRecordsTable = [sg.Table(values=adjacentRecords, key = 'tblPrevious',enable_events=False,  hide_vertical_scroll=True, headings=self.tableHeaders, max_col_width=32)]

        layout_bluearea = [broadGeo, taxonInput, barcode, [  # taxonomicPicklist,
            sg.Text('Record ID: ', key='lblRecordID', background_color='#99dcff', visible=True, size=(9, 1)),
            sg.Text('', key='txtRecordID', size=(4, 1), background_color=blueArea),
            sg.StatusBar('', relief=None, size=(7, 1), background_color=blueArea),
            sg.Button('SAVE', key="btnSave", button_color='seagreen', size=9),
            sg.StatusBar('', relief=None, size=(5, 1), background_color=blueArea),
            # sg.Button('First record', key="btnFirst", button_color='white on black',  font=('Arial', 8)),
            # sg.Button('Last record',  key="btnLast",  button_color='black on yellow', font=('Arial', 8)),
            sg.Button('GO BACK', key="btnBack", button_color='#8b0000'),
            sg.Button('GO FORWARDS', key='btnForward', button_color=('black', 'LemonChiffon2')),
            sg.Button('CLEAR FORM', key='btnClear', button_color='black on white'),
            # sg.Button('Export data', key='btnExport', button_color='royal blue'),  # Export data should be a backend feature says Pip
            # sg.Button('Dismiss', key='btnDismiss', button_color='white on black'), # Notifications not needed says Pip
        ], lblExport, previousRecordsTable]

        # Grey Area (Header) elements
        loggedIn = [
            sg.Text('Logged in as:', size=sessionInfoSize, background_color=greyArea, font=sessionInfoFont),
            sg.Text(gs.spUserName, key='txtUserName', size=(25, 1), background_color=greyArea, text_color='black',
                    font=smallLabelFont), ]
        
        institution_ = [
            sg.Text('Institution: ', size=sessionInfoSize, background_color=greyArea, font=sessionInfoFont),
            sg.Text(gs.institutionName, key='txtInstitution', size=(29, 1), background_color=greyArea,
                    font=smallLabelFont)]
        
        collection = [
            sg.Text('Collection:', size=sessionInfoSize, background_color=greyArea, text_color='black', font=sessionInfoFont),
            sg.Text(gs.collectionName, key='txtCollection', size=(25, 1), background_color=greyArea,
                    font=smallLabelFont)]
        
        version = [
            sg.Text(f"Version number: ", size=sessionInfoSize, background_color=greyArea, text_color='black',
                    font=sessionInfoFont),
            sg.Text(util.getVersionNumber(), size=(20, 1), background_color=greyArea, font=smallLabelFont,
                    text_color='black')]

        # Header section
        appTitle = sg.Text('Mass Annotation Digitization Desk (MADD)', size=(34, 3), background_color=greyArea, font=titleFont)
        settingsButton = sg.Button('SETTINGS', key='btnSettings', button_color='grey30')
        logoutButton = sg.Button('LOG OUT', key='btnLogOut', button_color='grey10')
        layoutTitle = [[appTitle], ]
        layoutSettingLogout = [sg.Push(background_color=greyArea), settingsButton, logoutButton]
        layoutMeta = [loggedIn, institution_, collection, version, layoutSettingLogout]

        # Combine elements into full layout - the first frame group is the grey metadata area.
        layout = [[
            sg.Frame('', layoutTitle, size=(550, 100), pad=(0, 0), background_color=greyArea, border_width=0),
            sg.Frame('', layoutMeta, size=(500, 120), pad=(0, 0), border_width=0, background_color=greyArea)],
            [sg.Frame('', [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250, 185),
                      background_color=greenArea, expand_x=True, ), ],  # expand_y=True,
            [sg.Frame('', [[sg.Column(layout_bluearea, background_color=blueArea)]],
                      title_location=sg.TITLE_LOCATION_TOP,
                      background_color=blueArea, expand_x=True, expand_y=True, )], ]  #

        # Launch window
        self.window = sg.Window("Mass Annotated Digitization Desk (MADD)", layout, margins=(2, 2), size=(1024, 540),
                                resizable=True, return_keyboard_events=True, finalize=True, background_color=greyArea)
        self.window.TKroot.focus_force() # Forces the app to be in focus.

        # Set session fields
        self.window.Element('txtUserName').Update(value=gs.spUserName)
        collection = self.db.getRowOnId('collection', collection_id)
        if collection is not None:
            self.window.Element('txtCollection').Update(value=collection[2])
            institution = self.db.getRowOnId('institution', collection[3])
            self.window.Element('txtInstitution').Update(value=institution[2])

        # Set triggers for the different controls on the UI form
        self.setControlEvents()

    def setControlEvents(self):
        # Set triggers for the different controls on the UI form

        # HEADER AREA
        self.window.Element('btnSettings').Widget.config(takefocus=0)
        self.window.Element('btnLogOut').Widget.config(takefocus=0)
        self.window.Element('txtUserName').Widget.config(takefocus=0)

        # GREEN AREA
        # cbxPrepType   # Combobox therefore already triggered
        # cbxTypeStatus # Combobox therefore already triggered
        self.window['txtNotes'].bind('<Tab>', '_Tab')
        #self.window['txtNotes'].bind('<Leave>', '_Edit') # Disabled because it would randomly activate the multispecimen checkbox when hovering over txtNotes
        self.window['chkMultiSpecimen'].bind("<Leave>", "_Edit")
        self.window['chkMultiSpecimen'].bind("<Return>", "_Enter")
        self.window['chkMultiSpecimen'].bind("<space>", '_space')

        # BLUE AREA
        # cbxGeoRegion  # Combobox therefore already triggered
        self.window['inpTaxonName'].bind("<Tab>", "_Tab")
        self.window['txtCatalogNumber'].bind('<Leave>', '_Edit')
        self.window['txtCatalogNumber'].bind("<Return>", "_Enter")
        self.window['btnSave'].bind("<Return>", "_Enter")


        #Block binds Focus events to all inputs.
        self.window['inpStorage'].bind('<FocusIn>', '_FocusIn')
        #self.window['inpStorage'].bind('<FocusOut>', '+focus out storage')
        self.window['cbxPrepType'].bind('<Click>', '_FocusIn')
        #self.window['cbxPrepType'].bind('<FocusOut>', '+focus out prepType')
        self.window['cbxTypeStatus'].bind('<Click>', '_FocusIn')
        #self.window['cbxTypeStatus'].bind('<FocusOut>', '+focus out typeStatus')
        self.window['txtNotes'].bind('<FocusIn>', '_FocusIn')
        #self.window['txtNotes'].bind('<FocusOut>', '+focus out notes')
        ##self.window['chkMultiSpecimen'].bind('<FocusIn>', '+focus in multispecimen')
        ##self.window['chkMultiSpecimen'].bind('<FocusOut>', '+focus out multispecimen')
        self.window['cbxGeoRegion'].bind('<Click>', '_FocusIn')
        #self.window['cbxGeoRegion'].bind('<FocusOut>', '+focus out BGR')
        #self.window['chkMultiSpecimen'].bind('<ButtonPress-1>', '+BTN1')
        self.window['inpTaxonName'].bind('<FocusIn>', '_FocusIn')
        #self.window['inpTaxonName'].bind('<FocusOut>', '+focus out taxon')
        self.window['txtCatalogNumber'].bind('<FocusIn>', '_FocusIn')
        #self.window['txtCatalogNumber'].bind('<FocusOut>', '+focus out catalog')

    def main(self):

        self.setFieldFocus('inpStorage') # Set focus on storage field
        self.window['inpStorage'].update(select=True) # Select all on field to enable overwriting pre-filled "None" placeholder
        self.window['tblPrevious'].update(values=self.recordSet.getAdjacentRecordList(self.tableHeaders)) # 
        
        while True:
            #self.window.Enable()
            # Main loop going through User Interface (UI) events 
            event, values = self.window.Read()
            #util.logger.debug(f'events: {event} | {values}')
            if event is None: break  # Empty event indicates user closing window

            if event == 'inpStorage':
                keyStrokes = values['inpStorage']
                #self.searchString.append(values[event])
                # If more than 3 characters entered:
                if len(keyStrokes) >=3 and keyStrokes != 'None': #len(self.searchString) >= 3:
                    self.HandleStorageInput(values['inpStorage'])

            elif event == '_Tab':  # This ensures that the notes field id written to the collection object.
                self.collobj.notes = values['txtNotes']
                # self.window['chkMultiSpecimen'].set_focus()

            elif event.endswith('+TAB'):
                self.window['cbxTypeStatus'].set_focus()
                # self.window['iconTypeStatus'].update(visible=True)

            elif event == 'cbxPrepType':
                self.collobj.setPrepTypeFields(self.window[event].widget.current())
                self.setFieldFocus('cbxTypeStatus')

            elif event == 'cbxTypeStatus':
                # TypeStatus is preloaded in the Class
                self.collobj.setTypeStatusFields(self.window[event].widget.current())
                self.collobj.typeStatusName = self.window['cbxTypeStatus'].get()
                self.setFieldFocus('txtNotes')

            elif event == 'txtNotes_Edit':
                self.collobj.notes = values['txtNotes']
                self.setFieldFocus('chkMultiSpecimen')

            elif event == 'chkMultiSpecimen':
                #   
                txtMultiSpecimenNewValue = ''
                if self.collobj.multiSpecimen == '':
                    # Multispecimen field not yet set: Unhide field and generate random name 
                    self.window['txtMultiSpecimen'].update(visible=True)    
                    txtMultiSpecimenNewValue = util.getRandomNumberString()
                else:
                    # Multispecimen field already set: Reset and hide text field
                    self.window['txtMultiSpecimen'].update(visible=False)
                    txtMultiSpecimenNewValue = ''                
                
                # Update field with new value and reflect on specimen record 
                self.window['txtMultiSpecimen'].update(value=txtMultiSpecimenNewValue)
                self.collobj.multiSpecimen = txtMultiSpecimenNewValue
                self.setFieldFocus('cbxGeoRegion')

            elif event == 'txtMultiSpecimen_Edit':
                self.collobj.multiSpecimen = values['txtMultiSpecimen']
                self.setFieldFocus('cbxGeoRegion')

            elif event == 'cbxGeoRegion':
                self.collobj.setGeoRegionFields(self.window[event].widget.current())
                self.setFieldFocus('inpTaxonName')

            elif event == 'inpTaxonName':

                # If more than 3 characters entered:
                if len(values[event]) >= 3:
                    # Get currently entered key strokes
                    keyStrokes = values['inpTaxonName']

                    self.autoTaxonName.Show()

                    # Fetch taxon name record from database based on user interactions with autosuggest popup window
                    selectedTaxonName = self.autoTaxonName.captureSuggestion(keyStrokes)

                    # Set taxon name fields using record retrieved
                    if selectedTaxonName is not None:
                        ''' Set specimen record taxon name fields
                            The selectedTaxonName manipulation is for the case when 
                            there is a novel family name and the object.notes come back with artifacts.'''
                        self.collobj.setTaxonNameFieldsFromModel(selectedTaxonName)                        

                        # Update UI to indicate selected taxon name record
                        self.window['inpTaxonName'].update(selectedTaxonName.fullName)

                        # Move focus further to next field (Barcode textbox)
                        self.setFieldFocus('txtCatalogNumber')

            elif event == 'txtCatalogNumber_Edit':
                self.collobj.catalogNumber = values['txtCatalogNumber']

            elif event == "txtCatalogNumber_Enter":
                self.collobj.catalogNumber = values['txtCatalogNumber']
                self.window['btnSave'].set_focus()
                self.setFieldFocus('')

            elif event == 'txtCatalogNumber':  # In production this will come from a barcode reader.
                self.collobj.catalogNumber = values[event]

            # **** Focus Events ****

            elif event.endswith('_FocusIn'):
                self.setFieldFocus(event[0:-8])

            # **** Button Events ****

            elif event == 'btnClear':
                # Clear all clearable fields as defined in list 'clearingFields'
                self.clearForm()

            elif event == 'btnBack':
                # Fetch previous specimen record data on basis of current record ID, if any
                record = self.collobj.loadPrevious(self.collobj.id)

                # If no further record back, retrieve current record (if any) or last record (if any)
                if not record:
                    # If there is a current record, reload current (meaning stay with current)
                    if self.collobj.id > 0:
                        record = self.collobj.load(self.collobj.id)
                    # Otherwise get latest record, if any
                    else: 
                        record = self.db.getLastRow('specimen', self.collectionId)
                        if record: 
                            self.collobj.setFields(record)
                        # If no records at all, this may indicate an empty table 
                
                # If a record has finally been retrieved, present content in data fields 
                if record:
                    self.fillFormFields(record)
                    
                    # Reload recordset and repopulate table of adjacent records 
                    self.recordSet.reload(record)
                    self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))
                    
                # Reset focus back to first field (Storage)
                self.setFieldFocus('inpStorage')

            elif event == 'btnForward':
                # First get current instance as record
                current = self.collobj.load()

                # Fetch next specimen record data on basis of current record ID, if any
                record = self.collobj.loadNext(self.collobj.id)
                
                # If a record has finally been retrieved, present content in data fields 
                if record:
                    self.fillFormFields(record)
                else:
                    # No further record: Prepare for blank record 
                    self.collobj = specimen.Specimen(self.collectionId)
                    self.clearNonStickyFields(values)

                    if current:        
                        # Transfer data in sticky fields to new record:
                        self.setRecordFields('specimen', current, True)

                # Reload recordset and repopulate table of adjacent records 
                self.recordSet.reload(record)
                self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))

                # Reset focus back to first field (Storage)
                self.setFieldFocus('inpStorage')

            elif event == 'btnExport':
                export_result = dx.exportSpecimens('xlsx')
                self.window['lblExport'].update(export_result, visible=True)

            elif event == 'btnDismiss':
                self.window['lblExport'].update(visible=False)
                self.window['lblRecordEnd'].update(visible=False)

            elif event == 'btnSave' or event == 'btnSave_Enter':
                self.SaveForm(values)

            elif event == 'btnFirst':
            #     self.getFirstOrLastRecord(position='first')
            #     #self.collobj.previousRecordEdit = True

            #     rowForTable = self.extractRowsInTwoFormats(record['id'])
            #     rowsAdjacent = rowForTable['adjacentrows']
            #     self.window['tblPrevious'].update(rowsAdjacent)
                pass

            elif event == 'btnLast':
            #     self.getFirstOrLastRecord(position='newest')
                pass
            
            # *** Close window Event
            
            elif event == sg.WINDOW_CLOSED:
                break

        self.window.close()

    def setFieldFocus(self, fieldName):
        """
        TODO 
        """

        #return  # Disable function
                
        # Iterate focus indicators and hide all 
        for field in self.focusIconList:
            self.window[field].update(visible=False)
        
        if fieldName != '':
            self.window[fieldName].set_focus()              # Set focus on field 
            #self.window[fieldName].update(select=True)      # Select all contents of field (TODO Doesn't work for combo lists)
            iconFieldName = 'icon' + fieldName[3:]          # Derive focus indicatorRight name 
            self.window[iconFieldName].update(visible=True) # Unhide focus indicatorRight
            #self.window[fieldName].update(background_color=self.highlight)
        # If fieldName is empty then all indicators are left unset 

        #self.window.Disable() # Attempt to escape infinite loop caused by Combo ...

        self.fieldInFocus = fieldName # (Re)set name of field in focus 
        util.logger.debug(f'set focus on: {fieldName}')

    def SaveForm(self, values):
        """
        TODO Function contract 
        """
        result = ''
        try:
            if len(self.notes) > 5:  
                # test to see if remark (verbatim note) was passed from autosuggest.
                self.collobj.notes = self.window['txtNotes'].Get() + ' | ' + self.notes
            else:
                self.collobj.notes = self.window['txtNotes'].Get()
            
            multispecimenName = self.window['txtMultiSpecimen'].get().strip()

            if values['chkMultiSpecimen'] == True:
                # If the multispecimen checkbox has been checked then the name field mustn't be empty ! 
                if multispecimenName != '':
                    self.collobj.multiSpecimen = multispecimenName
                else:
                    validationMessage = "Attempt to save with empty multispecimen name blocked!"
                    util.logger.error(validationMessage)
                    sg.PopupError(validationMessage)
                    return
            
            if values['txtCatalogNumber'] == '':
                # Barcode (catalog number) must not be empty!
                validationMessage = "Cannot leave barcode empty!"
                util.logger.error(validationMessage)
                sg.PopupError(validationMessage)
                return

            if len(values['txtCatalogNumber']) != 8:
                # Barcode (catalog number) must be 8 digits!
                validationMessage = "Barcode incorrect length (8)!"
                util.logger.error(validationMessage)
                sg.PopupError(validationMessage)
                return

            # Check if either updating existing or saving new record 
            if self.collobj.id == 0: newRecord = True
            else: newRecord = False

            # All checks out; Save specimen and clear non-sticky fields 
            savedRecord = self.collobj.save()

            # Remember id of record just save and prepare for blank record 
            previousRecordId = savedRecord['id'] # Id to be used for refreshing the previous rows table.

            if newRecord:            
                # Create a new, blank specimen record (id pre-set to 0)
                self.collobj = specimen.Specimen(self.collectionId)
                            
                # Transfer data in sticky fields to new record:
                self.setRecordFields('specimen', savedRecord, True)

                # Prepare form for next new record
                self.clearNonStickyFields(values)             
                self.setFieldFocus('txtCatalogNumber')
            else:
                # Existing record: Stay on record 

                pass
            
            # Refresh adjacent record set 
            self.recordSet.reload(savedRecord)
            self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))    

            result = "Successfully saved specimen record."

            util.logger.info(f'{result} : {previousRecordId} - {savedRecord}')

        except Exception as e:
            errorMessage = f"Error occurred attempting to save specimen: {e}"
            util.logger.error(errorMessage)
            sg.PopupError(e)
            result = errorMessage

        return result 
 
    def HandleStorageInput(self, keyStrokes):
        """
        TODO Function contract 
        """
        try:
            # Get currently entered key strokes
            #keyStrokes = self.searchString.pop()

            self.autoStorage.Show()

            # Fetch storage location record from database based on user interactions with autosuggest popup window
            selectedStorage = self.autoStorage.captureSuggestion(keyStrokes)

            # Set storage fields using record retrieved
            if selectedStorage is not None:
                # Set specimen record storage fields
                self.collobj.setStorageFieldsFromModel(selectedStorage)

                # Update UI to indicate selected storage record
                self.window['txtStorageFullname'].update(selectedStorage.fullName)
                self.window['inpStorage'].update(selectedStorage.name)

                # Move focus to next field (PrepTypes list). This is necessary due to all keys being captured
                # for the autoSuggest/capture_suggestion function.
            
            self.setFieldFocus('cbxPrepType')
        except Exception as e:
            util.logger.error(e)
            sg.PopupError(e)
        
        return ''

    def setSpecimenFields(self, stickyFieldsOnly=True):
        """
        TODO Method for synchronizing Model with View ... 
        """    
        # TODO Under construction
        return 

    def setRecordFields(self, tableName, record, stickyFieldsOnly=False):
        """
        Function for transferring information to fields of newly created record.
        CONTRACT:
            record : New record that should have its fields set
            stickyFieldsOnly : Flag for indicating whether only sticky fields should be set
        """
        
        self.collobj.setStorageFields(self.db.getRowOnId('storage', record['storageid']))
        self.collobj.setPrepTypeFields(self.window['cbxPrepType'].widget.current())
        self.collobj.setTypeStatusFields(self.window['cbxTypeStatus'].widget.current())
        self.collobj.notes = record['notes']
        self.collobj.notes = self.window['txtNotes'].get()
        self.collobj.multiSpecimen = record['multiSpecimen']
        self.collobj.setGeoRegionFields(self.window['cbxGeoRegion'].widget.current())
        self.collobj.setTaxonNameFields(self.db.getRowOnId('taxonname', record['taxonnameid']))

        if not stickyFieldsOnly:
            self.collobj.id = record['id']
            self.collobj.catalogNumber = record['catalognumber']

    def fillFormFields(self, record):
        """
        Function for setting form fields from specimen data record
        """
        self.window['txtRecordID'].update('{}'.format(record['id']), visible=True)
        self.window['inpStorage'].update(self.displayStorage(record['storagename']))
        self.window['txtStorageFullname'].update(record['storagefullname'])
        self.window['cbxPrepType'].update(record['preptypename'])
        # self.window['cbxHigherTaxon'].update('')
        self.window['cbxTypeStatus'].update(record['typestatusname'])
        self.window['txtNotes'].update(record['notes'])
        self.window['txtMultiSpecimen'].update(record['multispecimen'])
        if len(record['multispecimen']) > 2 : #Checks if txtMultiSpecimen is set.
            self.multiSpecimen = True
            self.window['chkMultiSpecimen'].update(True)
        else:
            self.multiSpecimen = False
            self.window['chkMultiSpecimen'].update(False)
        # self.window[''].update(multiSpecimen)
        self.window['cbxGeoRegion'].update(record['georegionname'])
        self.window['inpTaxonName'].update(record['taxonfullname'])
        self.window['txtCatalogNumber'].update(record['catalognumber'])

    def displayStorage(self, storageNameValue):
        if storageNameValue == '':
            return 'None'
        else:
            return storageNameValue

    def clearNonStickyFields(self, values):
        """
        Function for clearing all fields that are non-sticky
        """
        for key in self.nonStickyFields:
            field = self.window[key]
            field.update('')
        
        # Storage location is set to "None" to represent a blank entry in the UI
        self.window['inpStorage'].update('None')

    def clearForm(self):
        """
        Function for clearing all fields listed in clearing list and setting up for a blank record
        """
        # Clear fields defined in clearing list 
        for key in self.clearingList:
            self.window[key].update('')
        
        # Reset any information labels 
        self.window['lblExport'].update(visible=False)
        self.window['lblRecordEnd'].update(visible=False)

        # Set blank record 
        self.collobj = specimen.Specimen(self.collectionId)
        
        # Storage location is set to "None" to represent a blank entry in the UI
        self.window['inpStorage'].update('None')

    def getFirstOrLastRecord(self, position='first'):
        db = DataAccess(gs.databaseName)
        if position == 'first':
            sql = "SELECT min(id), * FROM specimen;"

            # lastRecord = db.getLastRow(tableName='specimen')
            firstRecord = db.executeSqlStatement(sql)
            self.window['tblPrevious'].update(firstRecord)
            self.fillFormFields(firstRecord[0])

        elif position == 'newest':
            newestRecord = db.getLastRow('specimen', self.collectionId)
            self.fillFormFields(newestRecord)
        else:
            util.logger.debug(f"Illegal argument in parameter 'position': {position} !")

        # Create new empty record accordingly 
        self.collobj = specimen.Specimen(self.collectionId)
    
