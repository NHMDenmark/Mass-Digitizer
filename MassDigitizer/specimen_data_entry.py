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

class SpecimenDataEntry():

    def __init__(self, collection_id):
        """
        Constructor that initializes class variables and dependent class instances 
        """
        
        self.versionNumber = util.getVersionNumber() # Get app version number for displaying
        self.collectionId = collection_id  # Set collection Id
        self.window = None  # Create class level instance of window object
        self.collobj = specimen.Specimen(collection_id)  # Create blank specimen record instance
        self.db = DataAccess(gs.databaseName)  # Instantiate database access module
        
        # TODO explanation due for below lines 
        #mxRow = self.db.getMaxRow('specimen') 
        #self.collobj.id = mxRow[0] 

        # self.retroRow = None  # Global to be used in step-back and other retrospective actions for saving.
        
        util.logger.info("Initializing Data Entry form for Institution & collection: %s | %s" % (gs.institutionName, gs.collectionName))
        
        # Various lists of fields to be cleared on command 
        self.clearingList = ['inpStorage', 'txtStorageFullname', 'cbxPrepType', 'cbxTypeStatus', 'txtNotes',
                             'chkMultiSpecimen', 'cbxGeoRegion', 'inpTaxonName', 'txtCatalogNumber', 'txtRecordID',
                             'txtMultiSpecimen']
        self.stickyFields = [{'txtStorageFullname'}, {'cbxPrepType'}, {'cbxTypeStatus'}, {'txtNotes'},
                             {'chkMultiSpecimen'}, {'txtMultiSpecimen'}, {'cbxGeoRegion'}, {'inpTaxonName'}]
        self.nonStickyFields = ['txtCatalogNumber', 'txtRecordID']

        # For arrow indicator use in window loop
        self.greenArea = '#E8F4EA'  # Stable fields
        self.blueArea = '#99ccff'  # Variable fields

        # Set up user interface 
        self.setup(collection_id)

        # Create class level notes for access in autoSuggest_popup (TODO ?)
        self.notes = ''

        # Gets the newest row by highest ID
        self.currentRecordId = self.window['txtRecordID'].get() # A check to see if UI is being "navigated" (btnBack/forward)
        if self.currentRecordId:
            pass
        else:
            pass
        self.maxRow = self.db.getMaxRow('specimen')[0]

        # Create auto-suggest popup window for storage locations
        self.autoStorage = autoSuggest_popup.AutoSuggest_popup('storage', collection_id)

        # Create auto-suggest popup window for taxon names
        self.autoTaxonName = autoSuggest_popup.AutoSuggest_popup('taxonname', collection_id)

        # Run 
        self.main()

    def setup(self, collection_id):
        """
        Initialize data entry form on basis of collection id
        """
        util.logger.info('*** Specimen data entry setup ***')

        # Define UI areas
        sg.theme('SystemDefault')
        greenArea = '#E8F4EA'  # Stable fields
        blueArea = '#99ccff'  # Variable fields
        greyArea = '#BFD1DF'  # Session & Settings

        # Set standard element dimensions
        defaultSize = (23, 1)  # Ensure element labels are the same size so that they line up
        element_size = (25, 1)  # Default width of all fields in the 'green area'
        green_size = (21, 1)  # Default width of all fields in the 'green area'
        blue_size = (35, 1)  # Default width of all fields in the 'blue area'
        storage_size = (22, 1)
        checkText_size = (20, 1)

        # Set text fonts
        captionFont = ('Bahnschrift', 13)
        fieldFont = ('Arial', 12) #
        labelHeadlineMeta = ('Bahnschrift', 12)
        titleFont = ('Bahnschrift', 18)
        smallLabelFont = ('Arial', 11, 'italic')
        wingding = ('Wingding', 18)
        indicator = '◀'

        # TODO placeholder For when higher taxonomic groups are added as filter
        taxonomicGroups = ['placeholder...']

        # NOTE Elements are stored  in variables to make it easier to include and position in the frames

        # Green Area elements
        storage = [
            sg.Text("Storage location:", size=storage_size, background_color=greenArea, font=captionFont),
            sg.InputText('None', key='inpStorage', focus=True, size=green_size, text_color='black', pad=(10,0),
                         background_color='white', font=fieldFont, enable_events=True),
            sg.Text(indicator, key='iconStorage', background_color=greenArea, visible=True, text_color=greenArea, font=wingding),
            sg.Text("", key='txtStorageFullname', size=(50, 2), background_color=greenArea, font=smallLabelFont),
            ]

        preparation = [
            sg.Text("Preparation type:", size=defaultSize, justification='l', background_color=greenArea, font=captionFont),
            sg.Combo(util.convert_dbrow_list(self.collobj.prepTypes), key='cbxPrepType', size=green_size,
                     text_color='black',
                     background_color='white', font=fieldFont, readonly=True, enable_events=True, pad=(0,0)),
                sg.Text(indicator, key='iconPrep', background_color=greenArea, visible=False, font=wingding)]

        type_status = [
            sg.Text('Type status:', size=defaultSize, background_color=greenArea, font=captionFont),
            sg.Combo(util.convert_dbrow_list(self.collobj.typeStatuses), key='cbxTypeStatus', size=green_size,
                     text_color='black',
                     background_color='white', font=fieldFont, readonly=True, enable_events=True, pad=(0,0)),
        sg.Text(indicator, pad=(7,0), key='iconType', background_color=greenArea, visible=False, font=wingding ),]
        notes = [
            sg.Text('Notes', size=defaultSize, background_color=greenArea, font=captionFont),
            sg.InputText(size=(80,5), key='txtNotes', background_color='white', text_color='black', pad=(0, 0),
                         enable_events=False, font=fieldFont),
            sg.Text(indicator, key='iconNotes', background_color=greenArea, visible=False, font=wingding)]

        multispecimen = [
            sg.Checkbox('Multispecimen object', key='chkMultiSpecimen', size=checkText_size, enable_events=True, background_color=greenArea, font=captionFont ), 
                         sg.InputText(size=(80,5), key='txtMultiSpecimen', background_color='white', text_color='black', pad=(3, 0), enable_events=True, font=fieldFont, visible=False), 
                         sg.Text(indicator, key='iconMulti', background_color=greenArea, visible=False, font=wingding)]

        layout_greenarea = [
            storage, preparation, type_status, notes, multispecimen, ]

        # Blue Area elements
        broadGeo = [
            sg.Text('Broad geographic region:', size=defaultSize, background_color=blueArea, text_color='black',
                    font=captionFont),
            sg.Combo(util.convert_dbrow_list(self.collobj.geoRegions), size=blue_size, key='cbxGeoRegion',
                     text_color='black',
                     background_color='white', font=fieldFont, readonly=True, enable_events=True),
                    sg.Text(indicator, key='iconBGR', background_color=blueArea, visible=False, font=wingding)]
        taxonInput = [
            sg.Text('Taxonomic name:     ', size=defaultSize, background_color=blueArea, text_color='black', font=captionFont),
            sg.Input('', size=blue_size, key='inpTaxonName', text_color='black', background_color='white',
                     font=fieldFont, enable_events=True, pad=((5, 0), (0, 0))),
            sg.Text(indicator, key='iconTaxon', background_color=blueArea, visible=False, font=wingding),
            sg.Text('No further record to go back to!', key='lblRecordEnd', visible=False, background_color="#ff5588",
                    border_width=3)]

        barcode = [
            sg.Text('Barcode:', size=defaultSize, background_color=blueArea, enable_events=True, text_color='black',
                    font=captionFont),
            sg.InputText('', key='txtCatalogNumber', size=blue_size, text_color='black', background_color='white',
                         font=fieldFont, enable_events=True), sg.Text(indicator, key='iconCatalog', background_color=blueArea, visible=False, font=wingding),]

        # statusLabel = [sg.Text('Specimen record has been saved', font=('Arial',20),size=(20,10),justification='center',background_color='#4f280a',text_color = 'yellow',key='texto')]

        self.headers = ['id', 'spid', 'catalognumber', 'multispecimen', 'taxonfullname', 'taxonname', 'taxonnameid',
                        'taxonspid', 'highertaxonname', 'preptypename', 'typestatusname', 'typestatusid',
                        'georegionname', 'georegionid', 'storagefullname', 'storagename']
        self.operationalHeads = ['id', 'catalognumber', 'taxonfullname', 'multispecimen',
                                 'georegionname', 'storagename', 'notes']
        # self.operationalHeads are headings for generating rows going into the previousRecordsTable


        # Records to be processed for display in the previousRecordsTable.
        self.previousRecords = self.previousRows()

        lblExport = [sg.Text('', key='lblExport', visible=False, size=(100, 2)), ]
        # previousRecordsTable = [
        #     sg.Table(values=self.previousRecords, key='tblPrevious', enable_events=True, headings=self.operationalHeads,
        #              max_col_width=32)]


        # self.tableRecords = self.previousRecords['adjacentrows']
        lblExport = [sg.Text('', key='lblExport', visible=False, size=(100, 2)), ]
        previousRecordsTable = [sg.Table(values=self.previousRecords, key = 'tblPrevious',enable_events=False,  hide_vertical_scroll=True, headings=self.operationalHeads, max_col_width=32)]


        layout_bluearea = [broadGeo, taxonInput, barcode, [  # taxonomicPicklist,
            sg.Text('Record ID: ', key='lblRecordID', background_color='#99dcff', visible=True, size=(9, 1)),
            sg.Text('', key='txtRecordID', size=(4, 1), background_color=blueArea),
            sg.StatusBar('', relief=None, size=(7, 1), background_color=blueArea),
            sg.Button('SAVE', key="btnSave", button_color='seagreen', size=9),
            sg.StatusBar('', relief=None, size=(5, 1), background_color=blueArea),
            # sg.Button('1st record', key="btn1st", button_color='white on black', font=('Arial', 8)),
            # sg.Button('newest record', key="btnNewest", button_color='black on yellow', font=('Arial', 8)),
            sg.Button('GO BACK', key="btnBack", button_color='#8b0000'),
            sg.Button('GO FORWARDS', key='btnForward', button_color=('black', 'LemonChiffon2')),
            sg.Button('CLEAR FORM', key='btnClear', button_color='black on white'),
            # sg.Button('Export data', key='btnExport', button_color='royal blue'),  # Export data should be a backend feature says Pip
            # sg.Button('Dismiss', key='btnDismiss', button_color='white on black'), # Notifications not needed says Pip
        ], lblExport, previousRecordsTable]

        # Grey Area (Header) elements
        loggedIn = [
            sg.Text('Logged in as:', size=(14, 1), background_color=greyArea, font=labelHeadlineMeta),
            sg.Text(gs.spUserName, key='txtUserName', size=(25, 1), background_color=greyArea, text_color='black',
                    font=smallLabelFont), ]
        institution_ = [
            sg.Text('Institution: ', size=(14, 1), background_color=greyArea, font=labelHeadlineMeta),
            sg.Text(gs.institutionName, key='txtInstitution', size=(29, 1), background_color=greyArea,
                    font=smallLabelFont)]
        collection = [
            sg.Text('Collection:', size=(14, 1), background_color=greyArea, text_color='black', font=labelHeadlineMeta),
            sg.Text(gs.collectionName, key='txtCollection', size=(25, 1), background_color=greyArea,
                    font=smallLabelFont)]
        version = [
            sg.Text(f"Version number: ", size=(14, 1), background_color=greyArea, text_color='black',
                    font=labelHeadlineMeta),
            sg.Text(self.versionNumber, size=(20, 1), background_color=greyArea, font=smallLabelFont,
                    text_color='black')]

        # Header section
        appTitle = sg.Text('Mass Annotation Digitization Desk (MADD)', size=(34, 3), background_color=greyArea,
                           font=titleFont)
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
        self.window.TKroot.focus_force()
        # Forces the app to be in focus.

        #Block binds Focus events to all inputs.
        self.window['inpStorage'].bind('<FocusIn>', '+focus in storage')
        self.window['inpStorage'].bind('<FocusOut>', '+focus out storage')
        self.window['cbxTypeStatus'].bind('<FocusIn>', '+focus in typeStatus')
        self.window['cbxTypeStatus'].bind('<FocusOut>', '+focus out typeStatus')
        self.window['cbxPrepType'].bind('<FocusIn>', '+focus in prepType')
        self.window['cbxPrepType'].bind('<FocusOut>', '+focus out prepType')
        self.window['txtNotes'].bind('<FocusIn>', '+focus in notes')
        self.window['txtNotes'].bind('<FocusOut>', '+focus out notes')
        self.window['chkMultiSpecimen'].bind('<FocusIn>', '+focus in multispecimen')
        self.window['chkMultiSpecimen'].bind('<FocusOut>', '+focus out multispecimen')
        self.window['cbxGeoRegion'].bind('<FocusIn>', '+focus in BGR')
        self.window['cbxGeoRegion'].bind('<FocusOut>', '+focus out BGR')
        self.window['chkMultiSpecimen'].bind('<ButtonPress-1>', '+BTN1')
        self.window['inpTaxonName'].bind('<FocusIn>', '+focus in taxon')
        self.window['inpTaxonName'].bind('<FocusOut>', '+focus out taxon')
        self.window['txtCatalogNumber'].bind('<FocusIn>', '+focus in catalog')
        self.window['txtCatalogNumber'].bind('<FocusOut>', '+focus out catalog')

        # Set session fields
        self.window.Element('txtUserName').Update(value=gs.spUserName)
        collection = self.db.getRowOnId('collection', collection_id)
        if collection is not None:
            self.window.Element('txtCollection').Update(value=collection[2])
            institution = self.db.getRowOnId('institution', collection[3])
            self.window.Element('txtInstitution').Update(value=institution[2])

        # Set triggers for the different controls on the UI form
        self.setControlEvents()
        # TODO Explain the functioning of searchString
        self.searchString = []

    def extractRowsInTwoFormats(self, rowId):
        """
        Returns a dict containing 3 rows prior to rowId (see self.db.getRows... statement)
        Return: A dict with two keys containing the complete rows:
        ('fullrows':) is a DICT
        and the rows for the 'adjacent' table:
         ('adjacentrows':) which is a LIST
        """
        # Considering moving this function to util.py or to a model class.
        #util.logger.debug('Extracting rows in two formats: %s' % rowId)

        rows = self.previousRows(rowId)
        headers = ['id', 'spid', 'catalognumber', 'multispecimen', 'taxonfullname', 'taxonname', 'taxonnameid',
                   'taxonspid',
                   'highertaxonname', 'typestatusname', 'typestatusid', 'georegionname', 'georegionid',
                   'storagefullname',
                   'storagename', 'storageid', 'preptypename', 'preptypeid', 'notes', 'institutionid', 'institutionname', 'collectionid', 'collectionname',
                   'username', 'userid', 'recorddatetime', 'exported', 'exportdatetime', 'exportuserid', 'agentfullname']
        # The order of the headers above is extremely important since there is a zip operation further down
        #  that creates the dictionary record. The header list and the row values list have to align correctly
        specimenList = [[row for row in line] for line in rows]

        # Code block below takes the rows returned and turns them into the complete row records and the previous row records.
        completeRowDicts = [] # full rows needed to populate the form
        previousRows = []  # the curated rows needed to populate the table
        for row in specimenList:
            specimenDict = dict(zip(headers, row)) # creates the complete row dict to be appended.
            #util.logger.debug('the specimen dict in for loop is: %s' % specimenDict)
            completeRowDicts.append(specimenDict)
            tempadjacent = []
            for k in self.operationalHeads:
                res = specimenDict[k]
                tempadjacent.append(res)
            previousRows.append(tempadjacent)
        rowsExtracted = {'fullrows': completeRowDicts, 'adjacentrows': previousRows}

        return rowsExtracted

    def previousRows(self, id=0, number=3):
        """ 
        Get previous three records based on current row's Id number (id=[integer]) or no keyword arg.
        Also feeds into the extractRowsInTwoFormats() function which is crucial.
        """
        try:
            if id > 0:
                filter = f"specimen WHERE id <= {id} AND collectionid = {self.collectionId}"

                rows = self.db.getRows(filter, limit=number, sortColumn='id DESC')
            else:
                rows = self.db.getRows('specimen', limit=number, sortColumn='id DESC')
            self.previousRecords = [[row for row in line] for line in rows]
        except Exception as e:
            util.logger.error(e)
            sg.PopupError(e)
        return self.previousRecords

    def main(self):
        # Checks to see where in the process the app state is in. TODO What does that mean? 
        if self.currentRecordId:  # if txtRecordId is set then...
            overviewRows = self.extractRowsInTwoFormats(self.currentRecordId)
        elif self.maxRow:  # when not 'stepped back' but specimen records do exist:
            overviewRows = self.extractRowsInTwoFormats(self.maxRow)
        else:  # Default state - an empty specimen table:
            overviewRows = {'adjacentrows': [[], [], []]}
        tblRows = list(overviewRows['adjacentrows'])
        #self.collobj.id = tblRows[0][0] # TODO WHY? This sets the collobj.id to be the last saved record… Why? 
        self.window['tblPrevious'].update(values=tblRows)
        self.window['inpStorage'].set_focus()
        self.window['inpStorage'].update(select=True)

        while True:
            event, values = self.window.Read()

            if event is None: break  # Empty event indicates user closing window

            # TODO Checking field events as a switch construct 

            if event == 'inpStorage':
                keyStrokes = values['inpStorage']
                self.searchString.append(values[event])
                # If more than 3 characters entered:
                if len(keyStrokes) >=3 and keyStrokes != 'None': #len(self.searchString) >= 3:
                    self.HandleStorageInput(values['inpStorage'])

            if event.endswith("focus in storage"):
                self.window['iconStorage'].update(text_color='black')

            if event.endswith("focus out storage"):
                self.window['iconStorage'].update(text_color=self.greenArea)

            if event.endswith("focus in prepType"):
                self.window['iconStorage'].update(text_color=self.greenArea)
                self.window['iconPrep'].update(visible=True)

            if event.endswith("focus out prepType"):
                self.window['iconPrep'].update(visible=False)

            if event.endswith("focus in typeStatus"):
                self.window['iconPrep'].update(visible=False)
                self.window['iconType'].update(visible=True) #hack to make indicator work

            if event.endswith("focus out typeStatus"):
                self.window['iconType'].update(visible=False)

            if event.endswith("focus in notes"):
                self.window['iconNotes'].update(visible=True)
                self.window['iconType'].update(visible=False)

            if event == '_Tab':  # This ensures that the notes field id written to the collection object.
                self.collobj.notes = values['txtNotes']
                # self.window['chkMultiSpecimen'].set_focus()

            if event.endswith('+TAB'):
                self.window['cbxTypeStatus'].set_focus()
                # self.window['iconType'].update(visible=True)

            if event == 'cbxPrepType':
                self.window['iconPrep'].update(visible=False)
                self.collobj.setPrepTypeFields(self.window[event].widget.current())
                self.window['iconPrep'].update(visible=False)
                self.window['cbxTypeStatus'].set_focus()
            elif event == 'cbxTypeStatus':
                # TypeStatus is preloaded in the Class
                self.collobj.setTypeStatusFields(self.window[event].widget.current())
                self.collobj.typeStatusName = self.window['cbxTypeStatus'].get()
                self.window['txtNotes'].set_focus()
            elif event == 'txtNotes_Edit':
                self.collobj.notes = values['txtNotes']
                self.window['chkMultiSpecimen'].set_focus()
            if event == 'chkMultiSpecimen':
                self.window['txtMultiSpecimen'].update('', visible=True)
                self.window['txtMultiSpecimen'].update(util.getRandomNumberString())
                
                self.collobj.multiSpecimen = values['txtMultiSpecimen']
                self.window['cbxGeoRegion'].set_focus()

            elif values['chkMultiSpecimen'] == False :
                # Resets the multi-specimen box
                self.window['txtMultiSpecimen'].update('')
                self.collobj.multiSpecimen = values['txtMultiSpecimen']

            elif event == 'chkMultiSpecimen_Edit':
                self.collobj.multiSpecimen = values['txtMultiSpecimen']

            if event.endswith("focus in multispecimen"):
                self.window['iconMulti'].update(visible=True)
                self.window['iconNotes'].update(visible=False) #Hack to make indicator arrow invisible

            if event.endswith("focus out multispecimen"):
                self.window['iconMulti'].update(visible=False)

            # if event.endswith("focus in BGR"):
            #     self.window['iconBGR'].update(visible=True)

            if event == 'cbxGeoRegion':
                self.collobj.setGeoRegionFields(self.window[event].widget.current())
                self.window['inpTaxonName'].set_focus()

            if event.endswith("focus in BGR"):
                self.window['iconBGR'].update(visible=True)

            if event.endswith("focus out BGR"):
                self.window['iconBGR'].update(visible=False)

            if event == 'inpTaxonName':

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
                        self.window['txtCatalogNumber'].set_focus()
                        # window['cbxTaxonName'].update(set_to_index=[0], scroll_to_index=0)

            if event.endswith("focus in taxon"):
                self.window['iconTaxon'].update(visible=True)

            if event.endswith("focus out taxon"):
                self.window['iconTaxon'].update(visible=False)
            elif event == 'txtCatalogNumber':  # In production this will come from a barcode reader.
                self.collobj.catalogNumber = values[event]

            if event.endswith("focus out catalog"):
                self.window['iconCatalog'].update(visible=False)

            if event.endswith("focus in catalog"):
                self.window['iconCatalog'].update(visible=True)

            elif event == 'txtCatalogNumber_Edit':
                self.collobj.catalogNumber = values['txtCatalogNumber']

            elif event == "txtCatalogNumber_Enter":
                self.collobj.catalogNumber = values['txtCatalogNumber']
                self.window['btnSave'].set_focus()

            elif event == 'btnClear':
                # Clear all clearable fields as defined in list 'clearingFields'
                self.clearForm()

            elif event == 'btnBack':
                # Fetch previous specimen record data on basis of current record ID, if any

                record = self.collobj.loadPrevious(self.collobj.id)
                if record:
                    # If not empty, set form fields
                    self.fillFormFields(record)
                    rowForTable = self.extractRowsInTwoFormats(record['id'])
                    rowsAdjacent = rowForTable['adjacentrows']
                    self.collobj.previousRecordEdit = True #Set a check to be used in save for edited records
                    self.window['tblPrevious'].update(rowsAdjacent)
                else:
                    # Indicate no further records
                    # self.window['lblRecordEnd'].update(visible=True)
                    self.collobj.previousRecordEdit = False #Unsets above check.
                self.window['inpStorage'].set_focus()

            elif event == 'btnForward':
                # Fetch next specimen record data on basis of current record ID, if any
                record = self.collobj.loadNext(self.collobj.id)

                if record:
                    # If not empty, set form fields
                    self.fillFormFields(record)
                    rowForTable = self.extractRowsInTwoFormats(record['id'])
                    rowsAdjacent = rowForTable['adjacentrows']
                    self.collobj.previousRecordEdit = True  #Set a check to be used in save for edited records.
                    self.window['tblPrevious'].update(rowsAdjacent)
                else:
                    # Indicate no further records
                    self.window['lblRecordEnd'].update(visible=False)
                    self.collobj.id = 0
                    self.collobj.previousRecordEdit = False #unsets above check.
                self.window['inpStorage'].set_focus()

            if event == 'btnExport':
                export_result = dx.exportSpecimens('xlsx')
                self.window['lblExport'].update(export_result, visible=True)

            if event == 'btnDismiss':
                self.window['lblExport'].update(visible=False)
                self.window['lblRecordEnd'].update(visible=False)

            if event == sg.WINDOW_CLOSED:
                break

            if event == 'tblPrevious':
                if values[event]:
                    # The table element has been activated
                    # Fetch previous records (again). Will fill the form with the row selected.
                    try:
                        recordAcute = self.previousRecords[values[event][0]] #The index position of the chosen record from the table
                        acuteID = recordAcute[0] # Pure integer value extracted.
                    except Exception as e:
                        util.logger.error(e)
                        sg.PopupError(e)
                    # TODO comment 
                    recordNow = self.extractRowsInTwoFormats(acuteID)
                    toSetRecord = recordNow['fullrows'][0]

                    self.window['txtMultiSpecimen'].update(visible=True)

                    self.collobj.setFields(toSetRecord)
                    # print('getfilds as dict=', self.collobj.getFieldsAsDict())

                    if self.collobj.id:
                        recordsAll = self.extractRowsInTwoFormats(self.collobj.id)
                        records = recordsAll['adjacentrows']
                    else:
                        records = overviewRows['adjacentrows'] # overviewRows comes from a check on the app state
                    multispecimenID = records[0][3]
                    recordAtSelectedIndex = records[0]

                    # Making three new records.
                    chosenRecordId = recordAtSelectedIndex[0]
                    # print(f'at newIndex:{newIndex} and at [0]:{newIndex[0]} + chosenID:{chosenRecordId} - recordSelectedIndex', recordAtSelectedIndex)
                    newRows = self.extractRowsInTwoFormats(chosenRecordId)

                    self.window['tblPrevious'].update(newRows['adjacentrows'])
                    self.window['inpStorage'].update(newRows['adjacentrows'][0])
                    retroRow = newRows['fullrows'][0]

                    self.fillFormFields(retroRow)

                    newRows = self.extractRowsInTwoFormats(chosenRecordId)

                    self.window['tblPrevious'].update(newRows['adjacentrows'])
                    self.window['inpStorage'].update(newRows['adjacentrows'][0])
                    self.retroRow = newRows['fullrows'][0]
                    self.fillFormFields(self.retroRow)

                else:
                    self.window['chkMultiSpecimen'].update(True)
                    self.window['txtMultiSpecimen'].update(multispecimenID)

            if event.endswith("focus out storage"):
                self.window['iconStorage'].update(text_color=self.greenArea)

            if event.endswith("focus out typeStatus"):
                self.window['iconType'].update(visible=False)

            if event.endswith("focus out prepType"):
                self.window['iconPrep'].update(visible=False)

            if event.endswith("focus out notes"):
                self.window['iconNotes'].update(visible=False)

            #Save form - augmented with a state check to see if
            # the record minted is an edit of an existing record or not.
            if event == 'btnSave' or event == 'btnSave_Enter':
                self.SaveForm(values)#, self.collobj.previousRecordEdit)
                self.window['inpStorage'].set_focus()

            if event == 'btn1st':
                self.getFirstOrLastRecord(position='first')
                self.collobj.previousRecordEdit = True

                rowForTable = self.extractRowsInTwoFormats(record['id'])
                rowsAdjacent = rowForTable['adjacentrows']
                self.window['tblPrevious'].update(rowsAdjacent)

            if event == 'btnNewest':
                self.getFirstOrLastRecord(position='newest')

        self.window.close()

    def SaveForm(self, values):
        """
        TODO Function contract 
        """
        # needs to loadCurrent from model.py to populate the collection object.
        # recordForSaving = self.collobj.loadCurrent(self.collobj.id)
        # self.collobj.setFields(recordForSaving)
        # save specimen and get its id
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

            # All checks out; Save specimen and clear non-sticky fields 
            savedRecord = self.collobj.save()
            #self.collobj.id = savedRecord[0]

            # Remember id of record just save and prepare for blank record 
            previousRecordId = savedRecord['id'] # Id to be used for refreshing the previous rows table.
            self.clearNonStickyFields(values) # Clear non-sticky to prepare form for blank record
            
            # Create a new, blank specimen record (id pre-set to 0)
            self.collobj = specimen.Specimen(self.collectionId)
                        
            # Transfer data in sticky fields to new record:
            self.setRecordFields('specimen', savedRecord, True)

            # Refresh records for tblPrevious after save.
            refreshedRecords = self.extractRowsInTwoFormats(previousRecordId)
            previousRefreshedRows = refreshedRecords['adjacentrows']
            self.window['tblPrevious'].update(previousRefreshedRows)
            # Transfer data in sticky fields to new record:
            self.setRecordFields('specimen', savedRecord, True)
            self.collobj.id = 0  # resets the record ID which makes it possible for the collection object to create a new record rather than to update the current one.

            self.window['txtCatalogNumber'].set_focus()

            result = "Successfully saved specimen record."

        except Exception as e:
            errorMessage = f"Error occurred attempting to save specimen: {e}"
            util.logger.error(errorMessage)
            sg.PopupError(e)
            result = errorMessage

        #self.collobj.id = savedRecord[0]
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
                self.window['cbxPrepType'].set_focus()
        except Exception as e:
            util.logger.error(e)
            sg.PopupError(e)
        
        return ''

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
        self.window['txtNotes'].bind('<Leave>', '_Edit')
        self.window['chkMultiSpecimen'].bind("<Leave>", "_Edit")
        self.window['chkMultiSpecimen'].bind("<Return>", "_Enter")
        self.window['chkMultiSpecimen'].bind("<space>", '_space')

        # BLUE AREA
        # cbxGeoRegion  # Combobox therefore already triggered
        self.window['inpTaxonName'].bind("<Tab>", "_Tab")
        self.window['txtCatalogNumber'].bind('<Leave>', '_Edit')
        self.window['txtCatalogNumber'].bind("<Return>", "_Enter")
        self.window['btnSave'].bind("<Return>", "_Enter")

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
        Function for clearing all fields listed in clearing list
        """
        # self.window['txtCatalogNumber'].update('')
        for key in self.clearingList:
            self.window[key].update('')
        self.window['lblExport'].update(visible=False)
        self.window['lblRecordEnd'].update(visible=False)
        self.searchString = []
        
        # Storage location is set to "None" to represent a blank entry in the UI
        self.window['inpStorage'].update('None')

    def getFirstOrLastRecord(self, position='first'):
        db = DataAccess(gs.databaseName)
        if position == 'first':
            sql = "SELECT min(id), * FROM specimen;"

            # lastRecord = db.getMaxRow(tableName='specimen')
            # print('maxRow:', [j for j in lastRecord])
            firstRecord = db.executeSqlStatement(sql)
            self.window['tblPrevious'].update(firstRecord)
            self.fillFormFields(firstRecord[0])

        elif position == 'newest':
            newestRecord = db.getMaxRow('specimen')
            self.fillFormFields(newestRecord)
        else:
            util.logger.debug(f"Illegal argument in parameter 'position': {position} !")

        # Create new empty record accordingly 
        self.collobj = specimen.Specimen(self.collectionId)
    
