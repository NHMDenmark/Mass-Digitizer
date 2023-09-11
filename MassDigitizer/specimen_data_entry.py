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
from models import recordset
from models import collection as coll
from models import model
import NHMA_lookup as lookup                

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
        self.collection = coll.Collection(collection_id)
        self.window = None  # Create class level instance of window object
        self.db = data_access.DataAccess(gs.databaseName)  # Instantiate database access module
        self.collobj = specimen.Specimen(collection_id)  # Create blank specimen record instance

        # Create recordset of last 3 saved records for the initial preview table
        self.recordSet = recordset.RecordSet(collection_id, 3,specimen_id=self.collobj.id) 

        # A switch to place the process in a state of 'freshness'. If initial then tab behavior is affected to go araound all fields.

        # Various lists of fields to be cleared on command
        # Needs radio in the input field list
        self.inputFieldList = ['inpStorage', 'cbxPrepType', 'cbxTypeStatus', 'chkDamage', 'inpNotes', 'radRadioSSO', 'radRadioMSO', 'radRadioMOS', 'inpContainerID', 'cbxGeoRegion', 'inpTaxonName', 'inpNHMAid', 'inpCatalogNumber', 'btnSave']
        self.inputFieldListSSO = ['inpStorage', 'cbxPrepType', 'cbxTypeStatus', 'inpNotes', 'inpCatalogNumber']
        self.focusIconList = ['inrStorage', 'inrPrepType', 'inrTypeStatus', 'inrDamage', 'inrNotes', 'inrRadioSSO', 'inrRadioMSO', 'inrRadioMOS', 'inrContainerID', 'inrGeoRegion', 'inrTaxonName', 'inrNHMAid', 'inrCatalogNumber', 'inrSave']
        self.focusIconListSSO = ['inrStorage', 'inrPrepType', 'inrTypeStatus', 'inrNotes', 'inrCatalogNumber']
        self.clearingList = ['inpStorage', 'txtStorageFullname', 'cbxPrepType', 'cbxTypeStatus', 'inpNotes','inpContainerID', 'cbxGeoRegion', 'inpTaxonName', 'inpNHMAid', 'inpCatalogNumber','txtRecordID']
        self.stickyFields = [{'txtStorageFullname'}, {'cbxPrepType'}, {'cbxTypeStatus'}, {'inpNotes'},{'inpContainerID'},{'cbxGeoRegion'}, {'inpTaxonName'}, {'inpNHMAid'}]
        self.nonStickyFields = ['inpCatalogNumber', 'txtRecordID', 'chkDamage']

        # Global variables
        self.barcodeList = []
        self.notes = ''  # Notes for access in autoSuggest_popup
        self.fieldInFocus = ''  # Stores name of field currently in focus
        self.fieldInFocusIndex = -1  # Stores list index of field currently in focus
        self.fieldname = ''
        self.input_list = None
        self.needsrepair = False

        # Create auto-suggest popup windows
        self.autoStorage = ''  # global for storage locations
        self.autoTaxonName = None  # global for taxon names
        self.taxonNameList = []

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

        r_title = sg.Text('Container type', size=captionSize, background_color=greenArea, font=captionFont)
        r_singleSpecimenObject = sg.Radio('Single specimen object', 'multi', default=True, enable_events=True, key="radRadioSSO", background_color=greenArea)
        r_multiSpecimenObject = sg.Radio('Multiple specimens on one object', 'multi', enable_events=True, key="radRadioMSO", background_color=greenArea)
        r_multiObjectSpecimen = sg.Radio('One specimen on multiple objects', 'multi', enable_events=True, key="radRadioMOS", background_color=greenArea)

        # multispecimenIdInput = [sg.InputText(size=(35,5), key='inpMultiSpecimen', background_color='white', text_color='black', pad=(3, 0), enable_events=True, font=fieldFont, visible=False)]
        #     sg.Text(indicatorRight,   key='inrMultiSpecimen', background_color=greenArea, visible=False, font=wingdingFont)]

        # Radio buttons for the three different container types

        multiRadio = [r_title,
                      r_singleSpecimenObject,
                      sg.Text(indicatorRight, key='inrRadioSSO', background_color=greenArea, visible=False, font=wingdingFont),
                      r_multiSpecimenObject,
                      sg.Text(indicatorRight, key='inrRadioMSO', background_color=greenArea, visible=False, font=wingdingFont),
                      r_multiObjectSpecimen,
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
            sg.Text('Taxonomic ID:', key='txtNHMAid', font=captionFont, background_color=blueArea, text_color='black', visible=False),
            sg.InputText('', size=(7, 1), key='inpNHMAid', text_color='black', background_color='white', font=fieldFont, enable_events=True, visible=False),
            sg.Text(indicatorRight, key='inrNHMAid', background_color=blueArea, visible=True, font=wingdingFont),
            sg.Text('No further record to go back to!', key='lblRecordEnd', visible=False, background_color="#ff5588", border_width=3)
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

        lblExport = [sg.Text('', key='lblExport', visible=False, size=(100, 2)), ]
        adjacentRecords = self.recordSet.getAdjacentRecordList(self.tableHeaders)
        previousRecordsTable = [
            sg.Table(values=adjacentRecords, key='tblPrevious', enable_events=False, hide_vertical_scroll=True,headings=self.tableHeaders, font=('Arial', 13), justification='left', auto_size_columns=True, max_col_width=28, select_mode=sg.TABLE_SELECT_MODE_NONE)]

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
            sg.Text(gs.userName, key='txtUserName', size=(25, 1), background_color=greyArea, text_color='black',
                    font=smallLabelFont), ]

        institution_ = [
            sg.Text('Institution: ', size=sessionInfoSize, background_color=greyArea, font=sessionInfoFont),
            sg.Text(gs.institutionName, key='txtInstitution', size=(29, 1), background_color=greyArea,
                    font=smallLabelFont)]

        collection = [
            sg.Text('Collection:', size=sessionInfoSize, background_color=greyArea, text_color='black',
                    font=sessionInfoFont),
            sg.Text(gs.collectionName, key='txtCollection', size=(25, 1), background_color=greyArea,
                    font=smallLabelFont)]

        version = [
            sg.Text(f"Version number: ", size=sessionInfoSize, background_color=greyArea, text_color='black',
                    font=sessionInfoFont),
            sg.Text(util.getVersionNumber(), size=(20, 1), background_color=greyArea, font=smallLabelFont,
                    text_color='black')]

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
            [sg.Frame('', [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250, 240),
                      background_color=greenArea, expand_x=True, ), ],  # expand_y=True,
            [sg.Frame('', [[sg.Column(layout_bluearea, background_color=blueArea)]],
                      title_location=sg.TITLE_LOCATION_TOP, background_color=blueArea, expand_x=True,
                      expand_y=True, )], ]

        # Launch window
        self.window = sg.Window("Mass Annotated Digitization Desk (MADD)", layout, margins=(2, 2), size=(1048, 640),
                                resizable=True, return_keyboard_events=True, finalize=True, background_color=greyArea)
        self.window.TKroot.focus_force()  # Forces the app to be in focus.

        # Set session fields
        # self.winInpTaxon = self.window['inpTaxonName']
        # self.winInpTaxon.bind('<FocusOut>', 'Focus Out')
        self.window.Element('txtUserName').Update(value=gs.userName)
        collection = self.db.getRowOnId('collection', collection_id)
        if collection is not None:
            self.window.Element('txtCollection').Update(value=collection[2])
            institution = self.db.getRowOnId('institution', collection[3])
            self.window.Element('txtInstitution').Update(value=institution[2])

        if gs.collectionName == 'NHMA Entomology':
            self.window.Element('txtNHMAid').Update(visible=True)
            self.window.Element('inpNHMAid').Update(visible=True)

        # Set triggers for the different controls on the UI form
        self.setControlEvents()

    def setControlEvents(self):
        # Set triggers for the different controls on the UI form

        self.window.bind("<Tab>", "Tab")  # Catchall handler for [tab] key
        self.window.bind("<Shift-KeyPress-Tab>", "Shift-Tab")  # Same for [shift]+[tab]

        # HEADER AREA
        self.window.Element('btnSettings').Widget.config(takefocus=0)  # TODO explain
        self.window.Element('btnLogOut').Widget.config(takefocus=0)  # TODO explain
        self.window.Element('txtUserName').Widget.config(takefocus=0)  # TODO explain

        # GREEN AREA
        # cbxPrepType   # Combobox therefore already triggered
        # cbxTypeStatus # Combobox therefore already triggered
        # self.window['inpNotes'].bind('<Tab>', '_Tab')
        # self.window['inpNotes'].bind('<Leave>', '_Edit') # Disabled because it would randomly activate the multispecimen checkbox when hovering over inpNotes
        self.window['inpNotes'].bind('<Return>', '_Enter')
        # self.window['radRadioSSO'].bind("<FocusOut>", "FocusOut")

        # BLUE AREA
        # cbxGeoRegion  # Combobox therefore already triggered
        # self.window['inpTaxonName'].bind("<Tab>", "_Tab")
        self.window['inpCatalogNumber'].bind('<Leave>', '_Edit')
        self.window['inpCatalogNumber'].bind("<Return>", "_Enter")
        self.window['inpNHMAid'].bind("<Return>", "_Enter")
        self.window['btnSave'].bind("<Return>", "_Enter")
        self.window['inpTaxonName'].bind('<FocusOut>', '_FocusOutTax')

        # Input field focus events
        for Name in self.inputFieldList:
            eventName = ''
            if Name[0:3] == 'inp':
                eventName = '<FocusIn>'
            elif Name[0:3] == 'cbx':
                eventName = '<Click>'
            else: break
            self.window[Name].bind(eventName, '_FocusIn')
        self.window['inpNotes'].bind('<FocusOut>', '_FocusOut')

    def main(self):

        self.window['inpStorage'].update(select=True)  # Select all on field to enable overwriting pre-filled "None" placeholder
        self.setFieldFocus('inpStorage')  # Set focus on storage field
        previous3records = self.recordSet.getAdjacentRecordList(self.tableHeaders)
        self.window['tblPrevious'].update(values=previous3records)  

        while True:
            # Main loop going through User Interface (UI) events

            event, values = self.window.Read()  # Get UI event values
            util.logger.debug(f'events: {event} | {values}')

            if event is None: break  # Empty event indicates user closing window

            self.window['lblError'].update('Validation error',visible=False)

            if event == 'inpStorage':
                keyStrokes = values['inpStorage']
                # Activate autosuggest box, when more than 3 characters entered:
                if len(keyStrokes) >= 3 and keyStrokes != 'None':
                    self.handleStorageInput(values['inpStorage'])

            elif event == 'cbxPrepType':
                self.collobj.setPrepTypeFields(self.window[event].widget.current())
                self.setFieldFocus('cbxTypeStatus')

            elif event == 'cbxTypeStatus':
                # TypeStatus is preloaded in the Class
                self.collobj.setTypeStatusFields(self.window[event].widget.current())
                self.collobj.typeStatusName = self.window['cbxTypeStatus'].get()
                self.setFieldFocus('chkDamage')

            elif event == "chkDamage":
                self.needsrepair = self.window['chkDamage'].get()
                if self.needsrepair: 
                    self.collobj.objectCondition = "Needs repair"
                else: 
                    self.collobj.objectCondition = ""
                self.setFieldFocus('inpNotes')

            elif (event == 'inpNotes_Edit' or event == 'inpNotes_Enter'):
                self.collobj.notes = values['inpNotes']
                # self.setFieldFocus('radioSingle')

            elif event == 'inpNotes_FocusOut':
                self.collobj.notes = values['inpNotes']

            elif event == 'radRadioMSO':
                mKey = util.getRandomNumberString()

                MSOkey = 'MSO' + str(mKey)
                self.collobj.containertype = 'Multiple specimens on one object'
                self.collobj.containername = MSOkey.strip()
                self.window['inpContainerID'].update(value=MSOkey, disabled=False)
                #
                # self.radioSelector(values)
                self.window['cbxGeoRegion'].set_focus()
                self.window['inrGeoRegion'].update(visible=True)

            elif event == 'radRadioMOS':
                mKey = util.getRandomNumberString()
                MOSkey = 'MOS' + str(mKey)
                self.collobj.containertype = 'One specimen on multiple objects'
                self.collobj.containername = MOSkey.strip()
                self.window['inpContainerID'].update(value=MOSkey, disabled=False)

                # self.radioSelector(values)
                self.window['cbxGeoRegion'].set_focus()
                self.window['inrGeoRegion'].update(visible=True)

            elif event == 'radRadioSSO':
                self.window['inpContainerID'].update(value='')
                self.collobj.containername = ''
                self.collobj.containertype = ''

                self.window['radRadioMOS'].reset_group()
                self.window['radRadioSSO'].update(value=True)

            # elif event == 'chkMultiSpecimen' or event == 'chkMultiSpecimen_Enter':
            #     # When multispecimen checkbox is checked or enter is pressed while in focus:
            #     inpMultiSpecimenNewValue = ''
            #     if self.collobj.multiSpecimen == '':
            #         # Multispecimen field not yet set: Unhide field, check field and generate random name
            #         self.window['inpMultiSpecimen'].update(visible=True)
            #         self.window['chkMultiSpecimen'].update(True)  # Check
            #         inpMultiSpecimenNewValue = util.getRandomNumberString()
            #     else:
            #         # Multispecimen field already set: Reset and hide text field
            #         self.window['chkMultiSpecimen'].update(False)  # Uncheck
            #         self.window['inpMultiSpecimen'].update(visible=False)
            #         inpMultiSpecimenNewValue = ''
            #
            #         # Update field with new value and reflect on specimen record
            #     self.window['inpMultiSpecimen'].update(value=inpMultiSpecimenNewValue)
            #     self.collobj.multiSpecimen = inpMultiSpecimenNewValue
            #     self.setFieldFocus('cbxGeoRegion')

            # elif event == 'inpMultiSpecimen_Edit':
            #     self.collobj.multiSpecimen = values['inpMultiSpecimen']
            #     self.setFieldFocus('cbxGeoRegion')

            elif event == 'cbxGeoRegion':
                self.collobj.setGeoRegionFields(self.window[event].widget.current())
                self.setFieldFocus('inpTaxonName')

            elif event == 'inpTaxonName':
                keyStrokes = values['inpTaxonName'].rstrip("\n")
                if "\t" in keyStrokes:
                    # self.autoTrigger = 'Done'
                    cleanName = keyStrokes.replace("\t", '')
                    # ¤¤¤ End
                    self.window['inpTaxonName'].update(cleanName)
                    self.window['inpCatalogNumber'].set_focus()
                    self.window['inpTaxonName'].Update('')
                    self.setFieldFocus('inpNHMAid')
                self.taxonNameList.append(keyStrokes) #Activate autosuggest box, when three characters or more are entered.
                res = None
                if len(keyStrokes) >= 3 and keyStrokes != 'None':
                    res = self.handleTaxonNameInput(values['inpTaxonName'].rstrip("\n"))
                    # Artifact from barcode reader produces an appended "\n"
                if res == 'Done':
                    self.window['inpCatalogNumber'].set_focus()

            elif event == 'inpNHMAid_Enter':
                taxonomicFullName = self.window['inpNHMAid'].get()
                fullName = lookup.getFullName(taxonomicFullName)
                self.window['inpTaxonName'].update(fullName)

            elif event == 'inpCatalogNumber_Enter':
                # Respond to barcode being entered or scanned by setting corresponding field value
                self.collobj.catalogNumber = values['inpCatalogNumber']

                self.saveForm()

            # **** Focus Events ****

            elif event.endswith('_FocusIn'):
                self.setFieldFocus(event[0:-8])  # Remove "_FocusIn" from event so we get the actual fieldname

            # **** Button Events ****

            elif event == 'btnClear':
                # Clear all clearable fields as defined in list 'clearingFields'
                self.clearForm()

            elif event == 'btnBack':
                # Fetch previous specimen record data on basis of current record ID, if any
                #recID = self.window['txtRecordID'].get()
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
                    self.setContainerFields(record)
                    self.recordSet = recordset.RecordSet(self.collectionId, 3, specimen_id=self.collobj.id)
                    self.recordSet.reload(record)
                    self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))

                # Reload recordset and repopulate table of adjacent records
                # self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))
                # self.recordSet.reload(record)
                # self.window['tblPrevious'].update(self.recordSet.getAdjacentRecordList(self.tableHeaders))

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
                self.window['lblRecordEnd'].update(visible=False)
                self.window['lblError'].update('Validation error',visible=False)

            elif event == 'btnSave' or event == 'btnSave_Enter':  # Should btnSave_Enter be removed?
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

            # *** Close window Event
            elif event == sg.WINDOW_CLOSED:
                break
            
            # TODO Explain or remove below: 
            #if self.window['radRadioSSO']:
            #    self.window['inpContainerID'].update(disabled=True)

        self.window.close()

    def setContainerFields(self, record):
        if record['containername']:
            #containerName = util.readMultispecimenID(record).strip()
            containerName = record['containername']
            if containerName == 'Multiple specimens on one object':
                self.window.Element('radRadioMSO').Update(value=True)
                self.window['inpContainerID'].update(disabled=False)
            elif containerName == 'One specimen covering multiple objects':
                self.window.Element('radRadioMOS').update(value=True)
                self.window['inpContainerID'].update(disabled=False)
        else:
            self.window.Element('radRadioSSO').update(value=True)

    def setFieldFocus(self, fieldName):
        """
        Common method for shifting focus to a specified input field as picked from array self.inputFieldList
        CONTRACT
            fieldName (String) : Name of the input field to receive focus
        """

        # Iterate focus indicators and hide all
        for field in self.focusIconList:
            self.window[field].update(visible=False)

        # Iterate input fields and reset background colour
        for field in self.inputFieldList:
            if field[0:3] == 'inp':
                self.window[field].update(background_color='#ffffff')
                if self.window[field] == '\t':
                    sg.popup_error('Tab characters not allowed in this field: ' + field)

        # If field name has been specified shift focus:
        if fieldName != '':
            self.window[fieldName].set_focus()  # Set focus on field
            # self.window[fieldName].update(select=True)     # Select all contents of field (TODO Doesn't work for combo lists)
            indicatorName = 'inr' + fieldName[3:]  # Derive focus indicator name
            if fieldName[3:] == 'btn':  # In case we are on the Save-button
                indicatorName = 'inr' + fieldName[3:]
            self.window[indicatorName].update(visible=True)  # Unhide focus indicator
            if fieldName[0:3] == 'inp':
                self.window[fieldName].update(background_color='#ffffff')  # self.highlight) # TODO Disabled until we get comboboxes to work
            # TODO Comboboxes won't play nice and also allow for changing background colour
            elif fieldName[0:3] == 'cbx':
                self.window[fieldName].ttk_style.configure(self.window[fieldName].ttk_style_name,fieldbackground=self.highlight)

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
            result = ''
            #catalogNumber = record['catalognumber'].replace('"', '') # TODO Explain necessity of this

            # Make sure everything is read on immediate barcode scan
            taxonFullName = self.window['inpTaxonName'].get()
            taxonFullName = taxonFullName.rstrip()  # barcode scanner adds newline
            self.collobj.taxonFullName = taxonFullName
            taxonTableRecord = self.getTaxonNameRecord(taxonFullName)            
            if taxonTableRecord:
                self.collobj.taxonName = taxonTableRecord['name']
                self.collobj.taxonRankName = taxonTableRecord['taxonrank']
                self.collobj.familyName = self.collobj.searchParentTaxon(taxonTableRecord['name'], 140, self.collection.taxonTreeDefId)
                self.collobj.higherTaxonName = taxonTableRecord['name'].split(' ')[0]
                self.collobj.rankid = taxonTableRecord['rankid']
                self.collobj.taxonNameId = taxonTableRecord['id']
                self.collobj.taxonSpid = taxonTableRecord['spid']
                self.collobj.parentFullName = taxonTableRecord['parentfullname']

            recordIdFromForm = self.window['txtRecordID'].get()
            self.collobj.id

            if recordIdFromForm:
                newRecord = False
            else:
                newRecord = True

            # self.window['radRadioMOS'].reset_group()
            # self.window['radRadioSSO'].update(value=False)

            if newRecord:
                # Create a new, blank specimen record (id pre-set to 0)
                self.collobj.rankid = 0
                self.collobj.id = 0
                # Transfer data in sticky fields to new record:
                self.setSpecimenFields()
                # Prepare form for next new record
                self.clearNonStickyFields()

            if self.validateBarCode(self.collobj.catalogNumber):
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
                self.clearNonStickyFields()
            else:
                result = 'validation error'
                #sg.popup_error("Did not save due to validation error(s)!")

        except Exception as e:
            errorMessage = f"Error occurred attempting to save specimen: {e}"
            traceBack = traceback.format_exc()
            util.logger.error(errorMessage)
            sg.PopupError(f'{e} \n\n {traceBack}', title='Error handle storage input', )
            result = errorMessage

        # self.initialStep = False
        self.window['inpCatalogNumber'].set_focus()

        util.logger.info(f'{result}')
                         
        return result

    def validationFeedback(self, validationMessage):
        """Gives a validation feedback message to the user"""
        util.logger.error(validationMessage)
        sg.PopupTimed(validationMessage)

    def handleStorageInput(self, keyStrokes):
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
                # Set specimen record storage fields
                self.collobj.setStorageFieldsFromModel(selectedStorage)

                # Update UI to indicate selected storage record
                self.window['txtStorageFullname'].update(selectedStorage.fullName)
                self.window['inpStorage'].update(selectedStorage.name)
                self.window['inpStorage'].update(select=True)  # Select all characters in field
                self.collobj.storageFullName = selectedStorage.fullName
                # Move focus to next field (PrepTypes list).
                self.setFieldFocus('cbxPrepType')

        except Exception as e:
            util.logger.error(str(e))
            traceBack = traceback.format_exc()
            util.logger.error(traceBack)
            sg.popup_error(f'{e} \n\n {traceBack}', title='Error handle storage input', )

        return ''

    def handleTaxonNameInput(self, keyStrokes):
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
                # Set specimen record taxon name fields using record retrieved
                self.collobj.setTaxonNameFieldsUsingFullName(selectedTaxonName)

                # Update UI to indicate selected taxon name record
                self.window['inpTaxonName'].update(selectedTaxonName.fullName)

                # Add taxon name verbatim note to notes field and update UI field accordingly
                # if selectedTaxonName.notes != '':
                currentNotes = self.window['inpNotes'].get()

                # First strip off any previous new taxonomy notes
                if ' | Verbatim_taxon:' in currentNotes:
                    currentNotes = currentNotes.split(' | Verbatim_taxon:', 1)[0]
                # Add new taxonomy notes, if any
                self.collobj.notes = currentNotes + selectedTaxonName.notes

                self.window['inpNotes'].Update(self.collobj.notes)

                # Move focus further to next field (Barcode textbox)
                # self.setFieldFocus('inpCatalogNumber')

        except Exception as e:
            util.logger.error(str(e))
            traceBack = traceback.format_exc()
            util.logger.error(traceBack)
            sg.popup_error(f'{e} \n\n {traceBack}', title='Error handleTaxonNameInput', )

        return 'Done'

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
        self.collobj.setGeoRegionFields(self.window['cbxGeoRegion'].widget.current())
        taxonFullName = self.window['inpTaxonName'].get()
        taxonFullName = taxonFullName.rstrip()
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

    def getStorageRecord(self):
        """
        Retrieve storage record based on storage input field contents.
        Search is to be done on fullname since identical atomic values can occur across the storage tree with different parentage.
        """
        storageFullName = self.window['txtStorageFullname'].get()
        try:
            storageRecords = self.db.getRowsOnFilters('storage', {'fullname': f'="{storageFullName}"',
                                                                  'collectionid': f'={self.collectionId}'}, 1)
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
        CONTRACT:
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
            self.needsrepair = True
        else:
            self.needsrepair = False
        self.window['chkDamage'].update(self.needsrepair)
        self.window['inpNotes'].update(record['notes'])
        if record['containername']:  # If not strip() is applied to none
            self.window['inpContainerID'].update(record['containername'].strip())

        # multispecimen = record['multispecimen']
        # if multispecimen != '' and multispecimen is not None:
        #     # If multispecimen field has contents, set & unhide respective fields
        #     self.multiSpecimen = True
        #     self.window['chkMultiSpecimen'].update(True)
        #     self.window['inpMultiSpecimen'].update(visible=True)
        # else:
        #     # Multispecimen field is empty, clear & unhide respective fields
        #     self.multiSpecimen = False
        #     self.window['chkMultiSpecimen'].update(False)
        #     self.window['inpMultiSpecimen'].update(visible=False)
        self.window['cbxGeoRegion'].update(record['georegionname'])
        self.window['inpTaxonName'].update(record['taxonfullname'])
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
        self.window['inpStorage'].update('None')

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
        self.window['lblRecordEnd'].update(visible=False)
        self.window['radRadioMOS'].update(value=False)
        self.window['radRadioMSO'].update(value=False)
        self.window['radRadioSSO'].update(value=True)
        # self.initialStep = True

        # Set blank record
        self.collobj = specimen.Specimen(self.collectionId)

        # Storage location is set to "None" to represent a blank entry in the UI
        # self.window['inpStorage'].update('None')

    def getFirstOrLastRecord(self, position='first'):

        if position == 'first':
            sql = "SELECT min(id), * FROM specimen;"

            # lastRecord = db.getLastRow(tableName='specimen')
            firstRecord = self.db.executeSqlStatement(sql)
            self.window['tblPrevious'].update(firstRecord)
            self.fillFormFields(firstRecord[0])

        elif position == 'newest':
            newestRecord = self.db.getLastRow('specimen', self.collectionId)
            self.fillFormFields(newestRecord)
        else:
            util.logger.debug(f"Illegal argument in parameter 'position': {position} !")

        # Create new empty record accordingly
        self.collobj = specimen.Specimen(self.collectionId)

    def radioSelector(self, containerKey):
        # Takes a list of radio values and selects the true one for the collobj.

        mKey = util.getRandomNumberString()
        if containerKey['radRadioMSO']:
            MSOkey = 'MSO' + str(mKey)
            self.collobj.containertype = 'Multiple specimens on one object'
            self.collobj.containername = MSOkey.strip()
            self.window['inpContainerID'].update(value=MSOkey, disabled=False)
            # return self.collobj.containertype
        elif containerKey['radRadioMOS']:
            MOSkey = 'MOS' + str(mKey)
            self.collobj.containertype = 'One specimen on multiple objects'
            self.collobj.containername = MOSkey.strip()
            self.window['inpContainerID'].update(value=MOSkey, disabled=False)
        elif containerKey['radRadioSSO']:
            self.window['inpContainerID'].update(value='')
            self.collobj.containername = ''
            self.collobj.containertype = ''

        return self.collobj.containertype

    def validateBarCode(self, barcode):
        # Ensuring that the barcode has the correct length according to collection.
        validation = None
        
        if len(barcode) == self.collection.catalogNrLength:
            validation = True
        else:
            validation = False 
            #sg.popup_error("Catalog number has the wrong format!")
            self.window['lblError'].update('Validation error: Barcode wrong length!',visible=True)

        return validation

    def verifyCatalogNumber(self, catalogNumber):
        # Validates if barcode is digits
        if catalogNumber.isdigit():
            return 'valid'
        else:
            e = "Barcode/catalog number contains non numeric symbols."
            sg.PopupError(e)
            
