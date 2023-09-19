# -*- coding: utf-8 -*-

"""
Created
on Thu May 26 17:44:00 2022

@authors: Jan K. Legind, NHMD; Fedor A. Steeman NHMD

Copyright 2022 Natural History Museum of Denmark (NHMD)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.

CONVENTION :
'txt' in the element key means 'label'
'inp' in the element key means 'input field'
"""

import traceback
import PySimpleGUI as sg
import sys
# Internal dependencies
import util
import data_access
import global_settings as gs
import autoSuggest_popup
from models import specimen
from models import model
from models import recordset
from models import collection as coll

class SpecimenDataEntry():
    """
    Interface for entering specimen records.
    """

    def __init__(self, collection_id):
        """
        Constructor that initializes class variables and dependent class instances
        """
        util.logger.info("Initializing Data Entry form for Institution & collection: %s | %s" % (gs.institutionName, gs.collection.name))

        self.collectionId = collection_id  # Set collection Id
        self.collection = coll.Collection(collection_id)
        self.window = None  # Create class level instance of window object
        self.db = data_access.DataAccess(gs.databaseName)  # Instantiate database access module
        self.collobj = specimen.Specimen(collection_id)  # Create blank specimen record instance

        # Create recordset of last 3 saved records for the initial preview table
        self.recordSet = recordset.RecordSet(collection_id, 3,specimen_id=self.collobj.id) 

        # A switch to place the process in a state of 'freshness'. If initial then tab behavior is affected to go araound all fields.

        # Various lists of fields to be cleared on command
        # Needs radio in the input field list
        self.inputFieldList = ['inpStorage', 'cbxPrepType', 'cbxTypeStatus', 'chkDamage', 'inpNotes', 'radRadioSSO', 'radRadioMSO', 'radRadioMOS', 'inpContainerID', 'cbxGeoRegion', 'inpTaxonName', 'inpTaxonNumber', 'inpCatalogNumber', 'btnSave']
        self.inputFieldListSSO = ['inpStorage', 'cbxPrepType', 'cbxTypeStatus', 'inpNotes', 'inpCatalogNumber']
        self.focusIconList = ['inrStorage', 'inrPrepType', 'inrTypeStatus', 'inrDamage', 'inrNotes', 'inrRadioSSO', 'inrRadioMSO', 'inrRadioMOS', 'inrContainerID', 'inrGeoRegion', 'inrTaxonName', 'inrTaxonNumber', 'inrCatalogNumber', 'inrSave']
        self.focusIconListSSO = ['inrStorage', 'inrPrepType', 'inrTypeStatus', 'inrNotes', 'inrCatalogNumber']
        self.clearingList = ['inpStorage', 'txtStorageFullname', 'cbxPrepType', 'cbxTypeStatus', 'inpNotes','inpContainerID', 'cbxGeoRegion', 'inpTaxonName', 'inpTaxonNumber', 'inpCatalogNumber','txtRecordID']
        self.stickyFields = [{'txtStorageFullname'}, {'cbxPrepType'}, {'cbxTypeStatus'}, {'inpNotes'},{'inpContainerID'},{'cbxGeoRegion'}, {'inpTaxonName'}, {'inpTaxonNumber'}]
        self.nonStickyFields = ['inpCatalogNumber', 'txtRecordID', 'chkDamage']

        # Global variables
        self.fieldInFocus = ''  # Stores name of field currently in focus
        self.fieldInFocusIndex = -1  # Stores list index of field currently in focus
        self.MSOterm = 'Multiple specimens on one object'
        self.MOSterm = 'One specimen on multiple objects'

        # Create auto-suggest popup windows
        self.autoStorage = ''  # global for storage locations
        self.autoTaxonName = None  # global for taxon names

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
        blueArea = '#99ccff'  # Variable fields (?)
        greyArea = '#BFD1DF'  # Session & Settings

        # Set standard element dimensions
        captionSize = (22, 1)  # Ensure element labels (captions) are the same size so that they line up
        greenSize = (21, 1)  # Default width of all fields in the 'green area'
        blueSize = (35, 1)  # Default width of all fields in the 'blue area'
        sessionInfoSize = (14, 1)

        # Set text fonts
        titleFont = ('Bahnschrift', 18)
        captionFont = ('Bahnschrift', 13)
        fieldFont = ('Arial', 12)  #
        sessionInfoFont = ('Bahnschrift', 12)
        smallLabelFont = ('Arial', 11, 'italic')
        wingdingFont = ('Wingding', 12)

        # Set special characters
        indicatorRight = '◀'

        self.highlight = '#fff8e3'

        # NOTE Elements are stored  in variables to make it easier to include and position in the frames

        # Green Area elements
        storage = [
            sg.Text("Storage location:", size=(21, 1), background_color=greenArea, font=captionFont),
            # sg.Text(indicatorLeft, key='inlStorage', text_color='black', background_color=greenArea, visible=True, font=wingdingFont),
            sg.InputText('None', key='inpStorage', focus=True, size=greenSize, text_color='black', pad=(10, 0), background_color='white', font=fieldFont, enable_events=True),
            sg.pin(sg.Text(indicatorRight, key='inrStorage', background_color=greenArea, visible=True, font=wingdingFont)),
            # 'Pin' because otherwise it's placed right of next element
            sg.Text("", key='txtStorageFullname', size=(50, 2), background_color=greenArea, font=smallLabelFont)
        ]

        preparation = [
            sg.Text("Preparation type:", size=captionSize, justification='l', background_color=greenArea, font=captionFont),
            # sg.Text(indicatorLeft, key='inlPrepType', text_color='black', background_color=greenArea, visible=True, font=wingdingFont),
            sg.Combo(util.convert_dbrow_list(self.collobj.prepTypes), key='cbxPrepType', size=greenSize, text_color='black', background_color='white', font=fieldFont, readonly=True, enable_events=True, pad=(0, 0)),
            sg.Text(indicatorRight, key='inrPrepType', background_color=greenArea, visible=False, font=wingdingFont)
        ]

        type_status = [
            sg.Text('Type status:', size=captionSize, background_color=greenArea, font=captionFont),
            # sg.Text(indicatorLeft, key='inlTypeStatus', text_color='black', background_color=greenArea, visible=True, font=wingdingFont),
            sg.Combo(util.convert_dbrow_list(self.collobj.typeStatuses), key='cbxTypeStatus', size=greenSize, text_color='black', background_color='white', font=fieldFont, readonly=True, enable_events=True, pad=(0, 0)),
            sg.Text(indicatorRight, pad=(7, 0), key='inrTypeStatus', background_color=greenArea, visible=False, font=wingdingFont),
        ]

        damaged_specimen = [
            sg.Text('Damaged specimen:', size=(21, 1), background_color=greenArea, font=captionFont),
            sg.Checkbox('', key="chkDamage", background_color=greenArea, enable_events=True),
            sg.Text(indicatorRight, pad=(7, 0), key='inrDamage', background_color=greenArea, visible=False, font=wingdingFont)
        ]
        notes = [
            sg.Text('Notes', size=captionSize, background_color=greenArea, font=captionFont),
            # sg.Text(indicatorLeft, key='inlNotes', text_color='black', background_color=greenArea, visible=True, font=wingdingFont),
            sg.InputText(size=(80, 5), key='inpNotes', pad=(0, 0), enable_events=False, font=fieldFont, background_color='white', text_color='black'),
            sg.Text(indicatorRight, key='inrNotes', background_color=greenArea, visible=False, font=wingdingFont)
        ]

        # Radio buttons for the three different container types
        r_title = sg.Text('Container type', size=captionSize, background_color=greenArea, font=captionFont)
        r_singleSpecimenObject = sg.Radio('Single specimen object', 'multi', default=True, enable_events=True, key="radRadioSSO", background_color=greenArea)
        r_multiSpecimenObject = sg.Radio(self.MSOterm, 'multi', enable_events=True, key="radRadioMSO", background_color=greenArea)
        r_multiObjectSpecimen = sg.Radio(self.MOSterm, 'multi', enable_events=True, key="radRadioMOS", background_color=greenArea)
        
        multiRadio = [r_title,
                      r_singleSpecimenObject,
                      sg.Text(indicatorRight, key='inrRadioSSO', background_color=greenArea, visible=False, font=wingdingFont), r_multiSpecimenObject,
                      sg.Text(indicatorRight, key='inrRadioMSO', background_color=greenArea, visible=False, font=wingdingFont), r_multiObjectSpecimen,
                      sg.Text(indicatorRight, key='inrRadioMOS', background_color=greenArea, visible=False, font=wingdingFont)
                      ]

        containerID = [sg.Text('Container ID ', font=sessionInfoFont, background_color=greenArea, size=captionSize),
                       sg.InputText(size=(50, 5), key='inpContainerID', disabled=True, pad=(0, 0), enable_events=False, font=fieldFont, background_color='white', text_color='black'),
                       sg.Text(indicatorRight, key='inrContainerID', background_color=greenArea, visible=False, font=wingdingFont), ]

        layout_greenarea = [storage, preparation, type_status, damaged_specimen, notes, multiRadio, containerID]

        # Blue Area elements
        broadGeo = [
            sg.Text('Broad geographic region:', size=captionSize, background_color=blueArea, text_color='black', font=captionFont),
            # sg.Text(indicatorLeft, key='inlGeoRegion', text_color='black', background_color=blueArea, visible=True, font=wingdingFont),
            sg.Combo(util.convert_dbrow_list(self.collobj.geoRegions), key='cbxGeoRegion', size=blueSize, text_color='black', background_color='white', font=fieldFont, readonly=True, enable_events=True),
            sg.Text(indicatorRight, key='inrGeoRegion', background_color=blueArea, visible=False, font=wingdingFont)
        ]

        taxonInput = [
            sg.Text('Taxonomic name:     ', size=captionSize, background_color=blueArea, text_color='black',font=captionFont),
            # sg.Text(indicatorLeft, key='inlTaxonName', text_color='black', background_color=blueArea, visible=True, font=wingdingFont),
            sg.Multiline('', size=blueSize, key='inpTaxonName', rstrip=False, no_scrollbar=True, text_color='black', background_color='white',font=fieldFont, enable_events=True, pad=((5, 0), (0, 0))),

            sg.Text(indicatorRight, key='inrTaxonName', background_color=blueArea, visible=True, font=wingdingFont),
            sg.Text('Taxon Number:', key='txtTaxonNumber', font=captionFont, background_color=blueArea, text_color='black', visible=True),
            sg.InputText('', size=(7, 1), key='inpTaxonNumber', text_color='black', background_color='white', font=fieldFont, enable_events=True, visible=True),
            sg.Text(indicatorRight, key='inrTaxonNumber', background_color=blueArea, visible=True, font=wingdingFont),
            #sg.Text('No further record to go back to!', key='lblRecordEnd', visible=False, background_color="#ff5588", border_width=3)
        ]

        barcode = [
            sg.Text('Barcode:', size=captionSize, background_color=blueArea, enable_events=True, text_color='black', font=captionFont),
            # sg.Text(indicatorLeft, key='inlCatalogNumber', text_color='black', background_color=blueArea, visible=True, font=wingdingFont),
            sg.InputText('', key='inpCatalogNumber', size=blueSize, text_color='black', background_color='white', font=fieldFont, enable_events=True),
            sg.Text(indicatorRight, key='inrCatalogNumber', background_color=blueArea, visible=False,font=wingdingFont),
            sg.Text('Validation Error', key='lblError', visible=False, background_color="#ff5588", border_width=3)
        ]

        # statusLabel = [sg.Text('Specimen record has been saved', font=('Arial',20),size=(20,10),justification='center',background_color='#4f280a',text_color= 'yellow',key='texto')]

        self.tableHeaders = ['id', 'catalognumber', 'taxonfullname', 'containertype', 'georegionname','storagename']  # Headers for previousRecordsTable

        lblExport = [sg.Text('', key='lblExport', visible=False, size=(100, 2)), ]
        
        # Get data to populate previous records table:
        adjacentRecords = self.recordSet.getAdjacentRecordList(self.tableHeaders)
        previousRecordsTable = [sg.Table(values=adjacentRecords, key='tblPrevious', enable_events=False, hide_vertical_scroll=True,headings=self.tableHeaders, font=('Arial', 13), justification='left', auto_size_columns=True, max_col_width=28, select_mode=sg.TABLE_SELECT_MODE_NONE)]

        layout_bluearea = [broadGeo, taxonInput, barcode, [  # taxonomicPicklist,
            sg.Text('Record ID: ', key='lblRecordID', background_color='#99dcff', visible=True, size=(9, 1)),
            sg.Text('', key='txtRecordID', size=(4, 1), background_color=blueArea),
            sg.StatusBar('', relief=None, size=(7, 1), background_color=blueArea),
            sg.Button('SAVE', key="btnSave", button_color='seagreen', size=9),
            sg.Text('', key='inrSave', background_color=blueArea, visible=True),
            sg.StatusBar('', relief=None, size=(5, 1), background_color=blueArea),
            #sg.Button('First record', key="btnFirst", button_color='white on black',  font=('Arial', 8)),
            #sg.Button('Last record',  key="btnLast",  button_color='black on yellow', font=('Arial', 8)),
            sg.Button('GO BACK', key="btnBack", button_color='#8b0000'),
            sg.Button('GO FORWARDS', key='btnForward', button_color=('black', 'LemonChiffon2')),
            sg.Button('CLEAR FORM', key='btnClear', button_color='black on white'),
            #sg.Button('Export data', key='btnExport', button_color='royal blue'),  # Export data should be a backend feature says Pip
            #sg.Button('Dismiss', key='btnDismiss', button_color='white on black'), # Notifications not needed says Pip
        ], lblExport, previousRecordsTable]

        # Grey Area (Header) elements
        loggedIn = [
            sg.Text('Logged in as:', size=sessionInfoSize, background_color=greyArea, font=sessionInfoFont),
            sg.Text(gs.userName, key='txtUserName', size=(25, 1), background_color=greyArea, text_color='black', font=smallLabelFont), ]

        institution_ = [
            sg.Text('Institution: ', size=sessionInfoSize, background_color=greyArea, font=sessionInfoFont),
            sg.Text(gs.institutionName, key='txtInstitution', size=(29, 1), background_color=greyArea, font=smallLabelFont)]

        collection = [
            sg.Text('Collection:', size=sessionInfoSize, background_color=greyArea, text_color='black',
                    font=sessionInfoFont),
            sg.Text(self.collection.name, key='txtCollection', size=(25, 1), background_color=greyArea, font=smallLabelFont)]

        version = [
            sg.Text(f"Version number: ", size=sessionInfoSize, background_color=greyArea, text_color='black',
                    font=sessionInfoFont),
            sg.Text(util.getVersionNumber(), size=(20, 1), background_color=greyArea, font=smallLabelFont, text_color='black')]

        # Header section
        appTitle = sg.Text('Mass Annotated Digitization Desk', size=(34, 3), background_color=greyArea, font=titleFont)
        settingsButton = sg.Button('SETTINGS', key='btnSettings', button_color='grey30')
        logoutButton = sg.Button('LOG OUT', key='btnLogOut', button_color='grey10')
        layoutTitle = [[appTitle], ]
        layoutSettingLogout = [sg.Push(background_color=greyArea), settingsButton, logoutButton]
        layoutMeta = [loggedIn, institution_, collection, version, layoutSettingLogout]

        # Combine elements into full layout - the first frame group is the grey metadata area.
        layout = [[
            sg.Frame('', layoutTitle, size=(550, 100), pad=(0, 0), background_color=greyArea, border_width=0),
            sg.Frame('', layoutMeta, size=(500, 120), pad=(0, 0), border_width=0, background_color=greyArea)],
            [sg.Frame('', [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250, 240), background_color=greenArea, expand_x=True, ), ],  # expand_y=True,
            [sg.Frame('', [[sg.Column(layout_bluearea, background_color=blueArea)]], title_location=sg.TITLE_LOCATION_TOP, background_color=blueArea, expand_x=True, expand_y=True, )], ]

        # Launch window
        self.window = sg.Window("Mass Annotated Digitization Desk (MADD)", layout, margins=(2, 2), size=(1048, 640), resizable=True, return_keyboard_events=True, finalize=True, background_color=greyArea)
        self.window.TKroot.focus_force()  # Forces the app to be in focus.

        # Set session fields
        #self.winInpTaxon = self.window['inpTaxonName']
        #self.winInpTaxon.bind('<FocusOut>', 'Focus Out')
        self.window.Element('txtUserName').Update(value=gs.userName)
        collection = self.db.getRowOnId('collection', collection_id)
        if collection is not None:
            self.window.Element('txtCollection').Update(value=collection[2])
            institution = self.db.getRowOnId('institution', collection[3])
            self.window.Element('txtInstitution').Update(value=institution[2])

        if self.collection.useTaxonNumbers == True:
            self.window.Element('txtTaxonNumber').Update(visible=True)
            self.window.Element('inpTaxonNumber').Update(visible=True)
        else:
            self.window.Element('txtTaxonNumber').Update(visible=False)
            self.window.Element('inpTaxonNumber').Update(visible=False)     

        # Set triggers for the different controls on the UI form
        self.setControlEvents()

    def setControlEvents(self):
        # Set triggers for the different controls on the UI form

        self.window.bind("<Tab>", "Tab")  # Catchall handler for [tab] key
        self.window.bind("<Shift-KeyPress-Tab>", "Shift-Tab")  # Same for [shift]+[tab]
        self.window.bind("<Click>", "Click")  # Catchall handler for [Enter] event

        # HEADER AREA
        self.window.Element('btnSettings').Widget.config(takefocus=0)  # TODO explain
        self.window.Element('btnLogOut').Widget.config(takefocus=0)  # TODO explain
        self.window.Element('txtUserName').Widget.config(takefocus=0)  # TODO explain

        # GREEN AREA
        # cbxPrepType   # Combobox therefore already triggered
        # cbxTypeStatus # Combobox therefore already triggered
        # self.window['inpNotes'].bind('<Tab>', '_Tab')
        # self.window['inpNotes'].bind('<Leave>', '_Edit') # Disabled because it would randomly activate the multispecimen checkbox when hovering over inpNotes
        self.window['inpNotes'].bind('<Return>', '_Return')
        # self.window['radRadioSSO'].bind("<FocusOut>", "FocusOut")

        # BLUE AREA
        # cbxGeoRegion  # Combobox therefore already triggered
        # self.window['inpTaxonName'].bind("<Tab>", "_Tab")
        self.window['inpCatalogNumber'].bind('<Leave>', '_Edit')
        self.window['inpCatalogNumber'].bind("<Return>", "_Return")
        #self.window['inpTaxonNumber'].bind("<Leave>", "_Edit")
        self.window['inpTaxonNumber'].bind("<Return>", "_Edit")
        self.window['inpTaxonNumber'].bind("<Tab>", "_Edit")
        self.window['inpTaxonNumber'].bind("<FocusOut>", "_Edit")
        self.window['btnSave'].bind("<Return>", "_Return")

        # Input field focus events
        for Name in self.inputFieldList:
            eventName = ''
            if Name[0:3] == 'inp':
                eventName = '<FocusIn>'
            elif Name[0:3] == 'cbx':
                eventName = '<Click>'
            elif Name[0:3] == 'chk':
                eventName = '<Click>'
            self.window[Name].bind(eventName, '_FocusIn')
        self.window['inpNotes'].bind('<FocusOut>', '_FocusOut')

    def main(self):

        self.setFieldFocus('inpStorage')  # Set focus on storage field
        self.window['inpStorage'].update(select=True)  # Select all on field to enable overwriting pre-filled "None" placeholder

        while True:
            # Main loop going through User Interface (UI) events

            event, values = self.window.Read()  # Get UI event values
            util.logger.debug(f'events: {event} | {values}')

            if event is None: break  # Empty event indicates user closing window

            self.window['lblError'].update('Validation error',visible=False) # Clear error message label 

            if event == 'inpStorage':
                keyStrokes = values['inpStorage']
                # Activate autosuggest box, when more than 3 characters entered:
                if len(keyStrokes) >= 3 and keyStrokes != 'None':
                    self.autoSuggestStorage(values['inpStorage'])

            elif event == 'cbxPrepType':
                self.collobj.setPrepTypeFields(self.window[event].widget.current())
                self.setFieldFocus('cbxTypeStatus')

            elif event == 'cbxTypeStatus':
                self.collobj.setTypeStatusFields(self.window[event].widget.current())
                self.collobj.typeStatusName = self.window['cbxTypeStatus'].get()
                self.setFieldFocus('chkDamage')

            elif event == "chkDamage":
                needsrepair = self.window['chkDamage'].get()
                if needsrepair: 
                    self.collobj.objectCondition = "Needs repair"
                else: 
                    self.collobj.objectCondition = ""
                self.setFieldFocus('inpNotes')

            elif (event == 'inpNotes_Edit' or event == 'inpNotes_Return'):
                self.collobj.notes = values['inpNotes']
                # self.setFieldFocus('radioSingle')

            elif event == 'inpNotes_FocusOut':
                self.collobj.notes = values['inpNotes']

            elif event == 'radRadioMSO':
                mKey = util.getRandomNumberString()

                MSOkey = 'MSO' + str(mKey)
                self.collobj.containertype = self.MSOterm
                self.collobj.containername = MSOkey.strip()
                self.window['inpContainerID'].update(value=MSOkey, disabled=False)
                self.setFieldFocus('cbxGeoRegion')

            elif event == 'radRadioMOS':
                mKey = util.getRandomNumberString()
                MOSkey = 'MOS' + str(mKey)
                self.collobj.containertype = self.MOSterm
                self.collobj.containername = MOSkey.strip()
                self.window['inpContainerID'].update(value=MOSkey, disabled=False)
                self.setFieldFocus('cbxGeoRegion')

            elif event == 'radRadioSSO':
                self.window['inpContainerID'].update(value='', disabled=True)
                self.collobj.containername = ''
                self.collobj.containertype = ''
                self.window['radRadioMOS'].reset_group()
                self.window['radRadioSSO'].update(value=True)
                self.window['inpContainerID'].update('')
                self.setFieldFocus('cbxGeoRegion')

            elif event == 'cbxGeoRegion':
                self.collobj.setGeoRegionFields(self.window[event].widget.current())
                self.setFieldFocus('inpTaxonName')

            elif event == 'inpTaxonName':
                # 
                keyStrokes = values['inpTaxonName'].rstrip("\n") # NOTE Artifact from barcode reader produces an appended "\n"
                                
                # Ensure any tabs are kept from creeping into the taxon name entered 
                if "\t" in keyStrokes:
                    cleanName = keyStrokes.replace("\t", '')
                    self.window['inpTaxonName'].update(cleanName)
                                
                # Activate autosuggest box, when three characters or more are entered.
                if len(keyStrokes) >= 3 and keyStrokes != 'None':
                    result = self.autoSuggestTaxonName(keyStrokes) 
                
                    if result == 'Done':
                        # Taxon name retrieved move to next field depending on collection
                        # NOTE Disabled, because we'd just synchronize both taxon fields and move on to barcode field 
                        #if self.collection.useTaxonNumbers == True:
                        #    self.setFieldFocus('inpTaxonNumber')
                        #else:
                        self.setFieldFocus('inpCatalogNumber')
                
                if self.window['inpTaxonName'].get().strip() == '':
                    # taxon input field empty: Clear all taxon related fields
                    self.collobj.setTaxonNameFieldsFromModel(model.Model(self.collectionId))
                    self.setSpecimenFields(False)
                    self.window['inpTaxonNumber'].update('') # Clear taxon number input field
                    self.setFieldFocus('inpCatalogNumber')

            elif event == 'inpTaxonNumber_Edit':
                # 
                taxonNumber = self.window['inpTaxonNumber'].get()
                if taxonNumber != '':
                    taxonRecord = self.db.getRowsOnFilters('taxonname', {'idnumber':f'={taxonNumber}'}, 1)
                    if taxonRecord:
                        taxonName = model.Model(self.collectionId)
                        taxonName.setFields(taxonRecord[0])
                        self.window['inpTaxonName'].update(taxonName.fullName)
                        self.handleTaxonNameInput(taxonName)
                        self.setFieldFocus('inpCatalogNumber')
                    else:
                        self.validationFeedback('Could not find taxon with this number! (' + taxonNumber + ')')
                        self.window['inpTaxonNumber'].update('')

            elif event == 'inpCatalogNumber_Return':
                # Respond to barcode being entered or scanned by setting corresponding field value
                self.collobj.catalogNumber = values['inpCatalogNumber']
                # Save form fields to record
                self.saveForm()

            # **** Focus Events ****

            elif event.endswith('_FocusIn'):
                # A field is activated: Set new field focus
                self.setFieldFocus(event[0:-8])  # Remove "_FocusIn" from event so we get the actual fieldname

            # **** Button Events ****

            elif event == 'btnClear':
                # Clear all clearable fields as defined in list 'clearingFields'
                self.clearForm()

            elif event == 'btnBack':
                # Fetch previous specimen record data on basis of current record ID, if any
                record = self.collobj.loadPrevious()

                # If no further record back, retrieve current record (if any) or last record (if any)
                if not record:
                    # If there is a current record, reload current (meaning stay with current)
                    if self.collobj.id > 0:
                        record = self.collobj.load(self.collobj.id)
                    # Otherwise get latest record, if any
                    else:
                        record = self.db.getLastRow('specimen', self.collectionId)
                        # If no records at all, this may indicate an empty table

                # If a record has finally been retrieved, present content in data fields
                if record:
                    self.collobj.setFields(record)
                    self.fillFormFields(record)

                    # Reload recordset and repopulate table of adjacent records
                    self.recordSet.reload(record)
                    self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))

                # Reset focus back to first field (Storage)
                self.setFieldFocus('inpStorage')
                self.window['inpStorage'].update(select=True)  # Select all characters in field
                if record['id'] != self.collobj.id:
                    util.logLine('Record id does not match specimen id!')

            elif event == 'btnForward':
                # First get current instance as record
                record = self.collobj.loadNext()
                
                if not record:
                    # No further record: Prepare for blank record
                    self.collobj = specimen.Specimen(self.collectionId)
                    self.clearNonStickyFields()
                    # Transfer data in sticky fields to new record:
                    self.setSpecimenFields()
                else:
                    # If a record has finally been retrieved, present content in data fields
                    self.collobj.setFields(record)
                    self.fillFormFields(record)
                    
                    self.recordSet = recordset.RecordSet(self.collectionId, 3, specimen_id=self.collobj.id)
                    self.recordSet.reload(record)
                    self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))

                # Reload recordset and repopulate table of adjacent records
                #self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))
                #self.recordSet.reload(record)
                #self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))

                # Reset focus back to first field (Storage)
                self.setFieldFocus('inpStorage')
                self.window['inpStorage'].update(select=True)  # Select all characters in field

            elif event == 'btnExport':
                # Export data table to spreadsheet
                # export_result = dx.exportSpecimens('xlsx')
                # self.window['lblExport'].update(export_result, visible=True)
                pass

            elif event == 'btnDismiss':
                # Hide any error and other messages
                self.window['lblExport'].update(visible=False)
                #self.window['lblRecordEnd'].update(visible=False)
                self.window['lblError'].update('Validation error',visible=False)

            elif event == 'btnSave' or event == 'btnSave_Return':  # Should btnSave_Return be removed?
                # Save current specimen record to app database
                self.collobj.catalogNumber = values['inpCatalogNumber']
                self.saveForm()

            elif event == 'btnFirst':
                # Go to first record in db table
                #     self.getFirstOrLastRecord(position='first')
                #     #self.collobj.previousRecordEdit = True

                #     rowForTable = self.extractRowsInTwoFormats(record['id'])
                #     rowsAdjacent = rowForTable['adjacentrows']
                #     self.window['tblPrevious'].update(rowsAdjacent)
                pass

            elif event == 'btnLast':
                # Go to last record in db table
                #     self.getFirstOrLastRecord(position='newest')
                pass

            elif event == 'Tab':

                # When tabbing, find the next field in the sequence and set focus on that field

                if (self.fieldInFocusIndex >= 0):
                    # Increment index of field in focus unless it reached the end

                    if self.fieldInFocusIndex < len(self.inputFieldList) - 1:
                        fieldIndex = self.fieldInFocusIndex + 1

                    else:
                        fieldIndex = 0  # End of sequence: Loop around to first field

                    fieldName = self.inputFieldList[fieldIndex]
                    # if len(self.window[fieldName].get()) < 1: TODO for version with optimized behavior for tabbing.
                self.setFieldFocus(fieldName)

                # self.tabToInputField(1) # Move to next input field  # TODO common method for the above lines?

            elif event == 'Shift-Tab':
                # When tabbing, find the next field in the sequence and set focus on that field

                if self.fieldInFocusIndex >= 0:
                    # Increment index of field in focus unless it reached the end

                    if self.fieldInFocusIndex > 0:
                        fieldIndex = self.fieldInFocusIndex - 1
                    else:
                        fieldIndex = len(self.inputFieldList) - 1  # Beginning of sequence: Loop around to last field

                    fieldName = self.inputFieldList[fieldIndex]

                    self.setFieldFocus(fieldName)

                # self.tabToInputField(-1) # Move to preceding input field # TODO common method for the above lines?

            #elif event.endswith('_Tab'):
                # TODO Re-evaluate the need for this event originally set for inpTaxonName and inpNotes
            #    util.logger.debug(f'field {event[0:-4]} tabbed')

            elif event == 'Click':
                pass

            # *** Close window Event
            elif event == sg.WINDOW_CLOSED:
                break
            
            # TODO Explain or remove below: 
            #if self.window['radRadioSSO']:
            #    self.window['inpContainerID'].update(disabled=True)

        self.window.close()

    def setContainerFields(self, record):
        """
        Method for setting container-related input fields on the basis of the record passed to it. 
        CONTRACT
            record (SQLite Row) : Specimen record with the container-related fields
        """

        if record['containername'] and record['containername'] != '':
            # Container name set; multi-specimen assumed
            containerName = record['containername'] # Get container name 
            containerType = record['containertype'] # Get container type 

            if containerType == self.MSOterm:
                self.window.Element('radRadioMSO').update(value=True) # Set MSO radiobutton  
            elif containerType == self.MOSterm:
                self.window.Element('radRadioMOS').update(value=True) # Set MOS radiobutton
            else:
                self.window['lblError'].update('Something went wrong!',visible=True)
            
            self.window['inpContainerID'].update(containerName)
            self.window['inpContainerID'].update(disabled=False)
        else:
            # No container name set; single specimen assumed
            self.window.Element('radRadioSSO').update(value=True) # Set SSO radiobutton            
            self.window['inpContainerID'].update('')              # Clear container name input field 
            self.window['inpContainerID'].update(disabled=True)   # Disable container name input field 

    def setFieldFocus(self, fieldName):
        """
        Common method for shifting focus to a specified input field as picked from array self.inputFieldList
        CONTRACT
            fieldName (String) : Name of the input field to receive focus
        """

        # Iterate focus indicators and hide all
        for field in self.focusIconList:
            self.window[field].update(visible=False)

        # Iterate input fields and reset background colour | TODO Disabled until we can get comboboxes to work
        #for field in self.inputFieldList:
        #    if field[0:3] == 'inp':
        #        self.window[field].update(background_color='#ffffff')

        # If field name has been specified shift focus:
        if fieldName != '':
            self.window[fieldName].set_focus()  # Set focus on field
            # self.window[fieldName].update(select=True)     # Select all contents of field (TODO Doesn't work for combo lists)
            
            indicatorName = 'inr' + fieldName[3:]  # Derive focus indicator name

            #if fieldName[3:] == 'btn':  # In case we are on the Save-button
            #    indicatorName = 'inr' + fieldName[3:]
            
            self.window[indicatorName].update(visible=True)  # Unhide focus indicator

            # Change field background colour | TODO Disabled until we get comboboxes to work
            #if fieldName[0:3] == 'inp':
            #    self.window[fieldName].update(background_color='#ffffff')  # self.highlight) # 
            # TODO Comboboxes won't play nice and also allow for changing background colour
            #elif fieldName[0:3] == 'cbx':
            #    self.window[fieldName].ttk_style.configure(self.window[fieldName].ttk_style_name,fieldbackground=self.highlight)

            self.fieldInFocus = fieldName  # (Re)set name of field in focus
            self.fieldInFocusIndex = self.inputFieldList.index(fieldName)
        # If fieldName is empty then all indicators are left unset

        util.logger.debug(f'Shifted focus on input field: "{fieldName}"')

    def saveForm(self):
        """
        Saving specimen data to database including validation of form input fields.
        The contents of the form input fields should have been immediately been transferred to the fields of the specimen object instance.
        A final validation and transfer of selected input fields is still performed to ensure data integrity.
        """

        try:
            # Prepare for saving (new) record 
            result = ''
            newRecord = self.collobj.id == 0

            # Run validations 
            validated = self.validateBarCodeDigits(self.collobj.catalogNumber) and self.validateBarCodeLength(self.collobj.catalogNumber)

            if validated:
                # All checks out; Save specimen
                savedRecord = self.collobj.save()
                recs3 = self.recordSet.getAdjacentRecordList(self.tableHeaders)
                self.window['tblPrevious'].update(recs3)
                # Remember id of record just save and prepare for blank record
                previousRecordId = savedRecord['id']  # Id to be used for refreshing the previous rows table.

                # Refresh adjacent record set
                self.recordSet.reload(savedRecord)
                self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))

                result = "Successfully saved specimen record."

                util.logger.info(f'{result} : {previousRecordId} - {savedRecord}')

                # If so, prepare for new blank record
                if newRecord:
                    # Create a new, blank specimen record (id pre-set to 0)
                    self.collobj = specimen.Specimen(self.collectionId)                    

                    # Transfer data in sticky fields to new record:
                    self.setSpecimenFields()

                    # Prepare form for next new record
                    self.clearNonStickyFields()
            else:
                result = 'validation error'

        except Exception as e:
            errorMessage = f"Error occurred attempting to save specimen: {e}"
            traceBack = traceback.format_exc()
            util.logger.error(errorMessage)
            sg.Popup(f'{e} \n\n {traceBack}', title='Error handle storage input', )
            result = errorMessage

        # self.initialStep = False
        self.setFieldFocus('inpCatalogNumber')

        util.logger.info(f'{result}')
                         
        return result

    def autoSuggestStorage(self, keyStrokes):
        """
        Show autosuggest popup for Storage selection and handle input from that window.
        """
        self.autoStorage = autoSuggest_popup.AutoSuggest_popup('storage', self.collectionId)
        try:
            self.autoStorage.Show()

            # Fetch storage location record from database based on user interactions with autosuggest popup window
            selectedStorage = self.autoStorage.captureSuggestion(keyStrokes)
            self.autoStorage = None  # Reset autosuggest box

            # Set storage fields using record retrieved
            if selectedStorage is not None:
                self.handleStorageInput(selectedStorage)

        except Exception as e:
            util.logger.error(str(e))
            traceBack = traceback.format_exc()
            util.logger.error(traceBack)
            sg.popup_error(f'{e} \n\n {traceBack}', title='Error handle storage input', )

        return ''
    
    def handleStorageInput(self, storageRecord):
        """
        Handle selection of storage record by setting relevant fields, both in model and UI
        """
        # Set specimen record storage fields
        self.collobj.setStorageFieldsFromModel(storageRecord)

        # Update UI to indicate selected storage record
        self.window['txtStorageFullname'].update(storageRecord.fullName)
        self.window['inpStorage'].update(storageRecord.name)
        self.window['inpStorage'].update(select=True)  # Select all characters in field
        self.collobj.storageFullName = storageRecord.fullName
        # Move focus to next field (PrepTypes list).
        self.setFieldFocus('cbxPrepType')

    def autoSuggestTaxonName(self, keyStrokes):
        """
        Show autosuggest popup for Taxon Name selection and handle input from that window.
        """
        self.autoTaxonName = autoSuggest_popup.AutoSuggest_popup('taxonname', self.collectionId)
        try:
            self.autoTaxonName.Show()

            # Fetch taxon name record from database based on user interactions with autosuggest popup window
            selectedTaxonName = self.autoTaxonName.captureSuggestion(keyStrokes)

            self.autoTaxonName = None  # Reset autosuggest box

            if selectedTaxonName is not None: 
                self.handleTaxonNameInput(selectedTaxonName)

        except Exception as e:
            util.logger.error(str(e))
            traceBack = traceback.format_exc()
            util.logger.error(traceBack)
            sg.popup_error(f'{e} \n\n {traceBack}', title='Error autoSuggestTaxonName', )

        return 'Done'

    def handleTaxonNameInput(self, taxonName):
        """
        Handle selection of taxon name record by setting relevant fields, both in model and UI
        """
        # Set specimen record taxon name fields using record retrieved
        self.collobj.setTaxonNameFieldsFromModel(taxonName)

        # Update UI to indicate selected taxon name record
        self.window['inpTaxonName'].update(taxonName.fullName)
        self.window['inpTaxonNumber'].update(taxonName.idNumber)

        # Add taxon name verbatim note to notes field and update UI field accordingly
        # if selectedTaxonName.notes != '':
        currentNotes = self.window['inpNotes'].get()

        # First strip off any previous new taxonomy notes
        if ' | Verbatim_taxon:' in currentNotes:
            currentNotes = currentNotes.split(' | Verbatim_taxon:', 1)[0]
        # Add new taxonomy notes, if any
        self.collobj.notes = currentNotes + taxonName.notes

        self.window['inpNotes'].Update(self.collobj.notes)


    # def handleMultiSpecimenCheck(self, value):
    #     """
    #     Handle event from MultiSpecimen checkbox
    #     """
    #     inpMultiSpecimenNewValue = ''
    #     if self.collobj.multiSpecimen == '':
    #         # Multispecimen field not yet set: Unhide field and generate random name
    #         self.window['inpMultiSpecimen'].update(visible=True)
    #         inpMultiSpecimenNewValue = util.getRandomNumberString()
    #     else:
    #         # Multispecimen field already set: Reset and hide text field
    #         self.window['inpMultiSpecimen'].update(visible=False)
    #         inpMultiSpecimenNewValue = ''
    #
    #         # Update field with new value and reflect on specimen record
    #     self.window['inpMultiSpecimen'].update(value=inpMultiSpecimenNewValue)
    #     self.collobj.multiSpecimen = inpMultiSpecimenNewValue
    #     self.setFieldFocus('cbxGeoRegion')

    def setSpecimenFields(self, stickyFieldsOnly=True):
        """
        Method for synchronizing specimen data object instance (Model) with form input fields (View).
        CONTRACT
            stickyFieldsOnly (Boolean) : Indication of only sticky fields should be synchronized usually in case of a new blank record
        """

        # Set specimen object instance fields from input form
        self.collobj.setStorageFieldsFromRecord(self.getStorageRecord())
        self.collobj.setPrepTypeFields(self.window['cbxPrepType'].widget.current())
        self.collobj.setTypeStatusFields(self.window['cbxTypeStatus'].widget.current())
        self.collobj.notes = self.window['inpNotes'].get()
        self.collobj.containername = self.window['inpContainerID'].get()
        self.collobj.containertype = self.getContainerTypeFromInput()
        self.collobj.setGeoRegionFields(self.window['cbxGeoRegion'].widget.current())
        taxonFullName = self.window['inpTaxonName'].get()
        taxonFullName = taxonFullName.rstrip()
        if self.collection.useTaxonNumbers:
            self.collobj.taxonNumber = self.window['inpTaxonNumber'].get()
        self.collobj.setTaxonNameFields(self.getTaxonNameRecord(taxonFullName))
        
        # Include non-sticky fields usually in case of synchronizing an existing record
        if not stickyFieldsOnly:
            txtRecordId = self.window['txtRecordID'].get()
            if txtRecordId != '':
                recordId = int(txtRecordId)
            else:
                recordId = 0
            self.collobj.id = recordId
            self.collobj.catalogNumber = self.window['inpCatalogNumber'].get()
    
    def getContainerTypeFromInput(self):
        """
        TODO
        """
        containerType = '' #  'radRadioSSO'

        if self.window['radRadioMSO'].get():
            containerType = self.MSOterm
        elif self.window['radRadioMOS'].get():
            containerType = self.MOSterm

        return containerType

    def getStorageRecord(self):
        """
        Retrieve storage record based on storage input field contents.
        Search is to be done on fullname since identical atomic values can occur across the storage tree with different parentage.
        """
        storageFullName = self.window['txtStorageFullname'].get()
        try:
            storageRecords = self.db.getRowsOnFilters('storage', {'fullname': f'="{storageFullName}"', 'collectionid': f'={self.collectionId}'}, 1)
        except:
            e = sys.exc_info()[0] + ' from getStorageRecord'
            util.logger.error(e)
            return None
        if len(storageRecords) > 0:
            storageRecord = storageRecords[0]
        else:
            storageRecord = None

        return storageRecord

    def getTaxonNameRecord(self, taxonFullName):
        """
        Retrieve taxon name record based on taxon name input field contents.
        Search is to be done on taxon fullname and taxon tree definition derived from collection.
        """
        # taxonFullName = self.window['inpTaxonName'].get()
        # taxonRecords = self.db.getRowsOnFilters('taxonname', {'fullname': f'="{taxonFullName}"',
        #                                                       'treedefid': f'={self.collection.taxonTreeDefId}'}, 1)
        sql = f"SELECT * FROM taxonname WHERE fullname = '{taxonFullName}' AND treedefid = {self.collection.taxonTreeDefId} LIMIT 1;"
        taxonRecords = self.db.executeSqlStatement(sql)
        if len(taxonRecords) > 0:
            taxonRecord = taxonRecords[0]
        else:
            taxonRecord = None
        return taxonRecord

    def setRecordFields(self, record, stickyFieldsOnly=False):
        """
        Function for transferring information to fields of newly created record.
        CONTRACT:record['notes']
            record : New record that should have its fields set
            stickyFieldsOnly : Flag for indicating whether only sticky fields should be set
        """

        self.collobj.setStorageFieldsFromRecord(self.db.getRowOnId('storage', record['storageid']))
        self.collobj.setPrepTypeFields(self.window['cbxPrepType'].widget.current())
        self.collobj.setTypeStatusFields(self.window['cbxTypeStatus'].widget.current())
        self.collobj.notes = record['notes']
        self.collobj.notes = self.window['inpNotes'].get()
        # self.collobj.multiSpecimen = record['multiSpecimen']
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
        self.window['cbxTypeStatus'].update(record['typestatusname'])

        if record['objectcondition'] == 'Needs repair':
            self.window['chkDamage'].update(True)
        else:
            self.window['chkDamage'].update(False)

        self.window['inpNotes'].update(record['notes'])

        if record['containername']:  # If not strip() is applied to none
            self.window['inpContainerID'].update(record['containername'].strip())

        self.setContainerFields(record)

        self.window['cbxGeoRegion'].update(record['georegionname'])
        self.window['inpTaxonName'].update(record['taxonfullname'])
        if self.collection.useTaxonNumbers:
            self.window['inpTaxonNumber'].update(record['taxonnumber'])
        self.window['inpCatalogNumber'].update(record['catalognumber'])

    def displayStorage(self, storageNameValue):
        if storageNameValue == '':
            return 'None'
        else:
            return storageNameValue

    def clearNonStickyFields(self):
        """
        Function for clearing all fields that are non-sticky
        """
        for key in self.nonStickyFields:
            field = self.window[key]
            field.update('')

        # Storage location is set to "None" to represent a blank entry in the UI
        #self.window['inpStorage'].update('None')

        # TODO Reset containers? 

    def clearForm(self):
        """
        Function for clearing all fields listed in clearing list and setting up for a blank record
        """
        '''Setting focus on the storage field'''
        self.setFieldFocus('inpStorage')
        # Clear fields defined in clearing list
        for key in self.clearingList:
            self.window[key].update('')
        # Reset radio buttons

        # Reset any information labels and radio buttons
        self.window['lblExport'].update(visible=False)
        #self.window['lblRecordEnd'].update(visible=False)
        self.window['radRadioMOS'].update(value=False)
        self.window['radRadioMSO'].update(value=False)
        self.window['radRadioSSO'].update(value=True)
        # self.initialStep = True

        # Set blank record
        self.collobj = specimen.Specimen(self.collectionId)

        # Storage location is set to "None" to represent a blank entry in the UI
        # self.window['inpStorage'].update('None')

    def radioSelector(self, containerKey):
        # Takes a list of radio values and selects the true one for the collobj.

        mKey = util.getRandomNumberString()
        if containerKey['radRadioMSO']:
            MSOkey = 'MSO' + str(mKey)
            self.collobj.containertype = self.MSOterm
            self.collobj.containername = MSOkey.strip()
            self.window['inpContainerID'].update(value=MSOkey, disabled=False)
            # return self.collobj.containertype
        elif containerKey['radRadioMOS']:
            MOSkey = 'MOS' + str(mKey)
            self.collobj.containertype = self.MOSterm
            self.collobj.containername = MOSkey.strip()
            self.window['inpContainerID'].update(value=MOSkey, disabled=False)
        elif containerKey['radRadioSSO']:
            self.window['inpContainerID'].update(value='')
            self.collobj.containername = ''
            self.collobj.containertype = ''

        return self.collobj.containertype

    def validateBarCodeLength(self, barcode):
        # Ensure that the barcode has the correct length according to collection.
        validation = None
        
        if len(barcode) == self.collection.catalogNrLength:
            validation = True
        else:
            validation = False 
            self.validationFeedback('Validation error: Barcode wrong length!')

        return validation

    def validateBarCodeDigits(self, catalogNumber):
        # Validates if barcode is digits
        validation = None
        
        if catalogNumber.isdigit():
            validation = True
        else:
            validation = False
            self.validationFeedback("Barcode/catalog number contains non numeric symbols.")
        
        return validation 

    def validationFeedback(self, validationMessage):
        """Gives a validation feedback message to the user"""
        util.logger.error(validationMessage)
        sg.Popup(validationMessage)
            
