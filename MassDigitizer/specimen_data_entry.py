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

import os
import sys
import pathlib
import PySimpleGUI as sg

# Internal dependencies
import util
from data_access import DataAccess
import global_settings as gs
import data_exporter as dx
import autoSuggest_popup
import version_number
from models import specimen

# Makes sure that current folder is registrered to be able to access other app files
sys.path.append(str(pathlib.Path(__file__).parent.parent.joinpath('MassDigitizer')))
currentpath = os.path.join(pathlib.Path(__file__).parent, '')


class SpecimenDataEntry():

    def __init__(self, collection_id):
        """
        Constructor that initializes class variables and dependent class instances 
        """
        self.verionNumber = version_number.getVersionNumber()
        self.collectionId = collection_id # Set collection Id 
        self.window = None # Create class level instance of window object 
        self.collobj = specimen.specimen(collection_id) # Create blank specimen record instance 
        self.db = DataAccess(gs.databaseName) # Instantiate database access module

        # Various lists of fields to be cleared on command 
        self.clearingList = ['txtStorage', 'txtStorageFullname', 'cbxPrepType', 'cbxTypeStatus', 'txtNotes', 'chkMultiSpecimen', 'cbxGeoRegion', 'inpTaxonName', 'txtCatalogNumber', 'txtRecordID']
        self.stickyFields = [{'txtStorageFullname'}, {'cbxPrepType'}, {'cbxTypeStatus'}, {'txtNotes'}, {'chkMultiSpecimen'}, {'cbxGeoRegion'}, {'inpTaxonName'}]
        self.nonStickyFields = ['txtCatalogNumber', 'txtRecordID']

        # Set up user interface 
        self.setup(collection_id)

        # Create class level notes for access in autoSuggest_popup (TODO ?)
        self.notes = ''

        # Gets the newest row by highest ID
        self.currentRecordId = self.window['txtRecordID'].get()
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

        # Define UI areas
        sg.theme('SystemDefault')
        greenArea = '#E8F4EA'  # Stable fields
        blueArea = '#99ccff'  # Variable fields
        greyArea = '#BFD1DF'  # Session & Settings

        # Set standard element dimensions
        defaultSize = (21, 1)  # Ensure element labels are the same size so that they line up
        element_size = (25, 1)  # Default width of all fields in the 'green area'
        green_size = (20, 1)  # Default width of all fields in the 'green area'
        blue_size = (35, 1)  # Default width of all fields in the 'blue area'

        # Set text fonts
        font = ('Bahnschrift', 13)
        labelHeadlineMeta = ('Bahnschrift', 12)
        titleFont = ('Bahnschrift', 18)
        smallLabelFont = ('Arial', 11, 'italic')

        # TODO placeholder For when higher taxonomic groups are added as filter
        taxonomicGroups = ['placeholder...']

        # NOTE Elements are stored  in variables to make it easier to include and position in the frames

        # Green Area elements
        storage = [
            sg.Text("Storage location:", size=defaultSize, background_color=greenArea, font=font),
            sg.InputText('', key='txtStorage', size=green_size, text_color='black',
                        background_color='white', font=('Arial', 12), enable_events=True),
            sg.Text("", key='txtStorageFullname', size=(50, 2), background_color=greenArea, font=smallLabelFont)]

        preparation = [
            sg.Text("Preparation type:", size=defaultSize, background_color=greenArea, font=font),
            sg.Combo(util.convert_dbrow_list(self.collobj.prepTypes), key='cbxPrepType', size=green_size, text_color='black',
                    background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
        # taxonomy = [ #Currently not used
        #     sg.Text("Taxonomic group:", size=defaultSize, visible=False, background_color=greenArea, font=font),
        #     sg.Combo(taxonomicGroups, key='cbxHigherTaxon', visible=False, size=green_size, text_color='black',
        #             background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
        type_status = [
            sg.Text('Type status:', size=defaultSize, background_color=greenArea, font=font),
            sg.Combo(util.convert_dbrow_list(self.collobj.typeStatuses), key='cbxTypeStatus', size=green_size,
                    text_color='black',
                    background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
        notes = [
            sg.Text('Notes', size=defaultSize, background_color=greenArea, font=font),
            sg.InputText(size=(80, 5), key='txtNotes', background_color='white', text_color='black', enable_events=False)]

        multispecimen = [sg.Checkbox('Multispecimen sheet', key='chkMultiSpecimen', enable_events=True, background_color=greenArea, font=(11))]

        layout_greenarea = [
            storage, preparation, type_status, notes, multispecimen, ]

        # Blue Area elements
        broadGeo = [
            sg.Text('Broad geographic region:', size=defaultSize, background_color=blueArea, text_color='black', font=font),
            sg.Combo(util.convert_dbrow_list(self.collobj.geoRegions), size=blue_size, key='cbxGeoRegion', text_color='black',
                    background_color='white', font=('Arial', 12), readonly=True, enable_events=True), ]
        taxonInput = [
            sg.Text('Taxonomic name:     ', size=(21, 1), background_color=blueArea, text_color='black', font=font),
            sg.Input('', size=blue_size, key='inpTaxonName', text_color='black', background_color='white',
                    font=('Arial', 12), enable_events=True, pad=((5, 0), (0, 0))),
            sg.Text('No further record to go back to!', key='lblRecordEnd', visible=False, background_color="#ff5588",
                    border_width=3)]

        barcode = [
            sg.Text('Barcode:', size=defaultSize, background_color=blueArea, enable_events=True, text_color='black',
                    font=font),
            sg.InputText('', key='txtCatalogNumber', size=blue_size, text_color='black', background_color='white',
                        font=('Arial', 12), enable_events=True), ]

        # statusLabel = [sg.Text('Specimen record has been saved', font=('Arial',20),size=(20,10),justification='center',background_color='#4f280a',text_color = 'yellow',key='texto')]

        self.headers = ['id', 'spid', 'catalognumber', 'multispecimen', 'taxonfullname','taxonname', 'taxonnameid', 'taxonspid', 'highertaxonname', 'preptypename','typestatusname', 'typestatusid', 'georegionname', 'georegionid','storagefullname', 'storagename']
        self.operationalHeads = ['catalognumber', 'taxonfullname', 'multispecimen',
                                 'georegionname', 'storagename', 'notes']
        self.prev3Records = self.previousRows3()
        # self.tableRecords = self.prev3Records['adjacentrows']
        lblExport = [sg.Text('', key='lblExport', visible=False, size=(100, 2)), ]
        previousRecordsTable = [sg.Table(values=self.prev3Records, key = 'tblPrevious',enable_click_events=True, enable_events=True, headings=self.operationalHeads, max_col_width=32)]


        layout_bluearea = [broadGeo, taxonInput, barcode, [  # taxonomicPicklist,
            sg.Text('Record ID: ', key='lblRecordID', background_color='#99dcff', visible=True, size=(9, 1)),
            sg.Text('', key='txtRecordID', size=(4, 1), background_color=blueArea),
            sg.StatusBar('', relief=None, size=(7, 1), background_color=blueArea),
            sg.Button('SAVE', key="btnSave", button_color='seagreen', size=9),
            sg.StatusBar('', relief=None, size=(14, 1), background_color=blueArea),
            sg.Button('GO BACK', key="btnBack", button_color='firebrick', pad=(13, 0)),
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
            sg.Text(gs.institutionName, key='txtInstitution', size=(29, 1), background_color=greyArea, font=smallLabelFont)]
        collection = [
            sg.Text('Collection:', size=(14, 1), background_color=greyArea, text_color='black', font=labelHeadlineMeta),
            sg.Text(gs.collectionName, key='txtCollection', size=(25, 1), background_color=greyArea, font=smallLabelFont)]
        version = [
            sg.Text(f"Version number: ", size=(14,1), background_color=greyArea, text_color='black', font=labelHeadlineMeta),
            sg.Text(self.verionNumber, size=(20,1), background_color=greyArea, font=smallLabelFont, text_color='black')]

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
            [sg.Frame('', [[sg.Column(layout_greenarea, background_color=greenArea)]], size=(250, 175),
                    background_color=greenArea, expand_x=True, ), ],  # expand_y=True,
            [sg.Frame('', [[sg.Column(layout_bluearea, background_color=blueArea)]], title_location=sg.TITLE_LOCATION_TOP,
                    background_color=blueArea, expand_x=True, expand_y=True, )], ]  #

        # Launch window
        self.window = sg.Window("Mass Annotated Digitization Desk (MADD)", layout, margins=(2, 2), size=(1024, 530),
                        resizable=True, return_keyboard_events=True, finalize=True, background_color=greyArea)
        self.window.TKroot.focus_force()
        # Forces the app to be in focus.

        # Set session fields
        self.window.Element('txtUserName').Update(value=gs.spUserName)
        collection = self.db.getRowOnId('collection', collection_id)
        if collection is not None:
            self.window.Element('txtCollection').Update(value=collection[2])
            institution = self.db.getRowOnId('institution', collection[3])
            self.window.Element('txtInstitution').Update(value=institution[2])
       

        # Set triggers for the different controls on the UI form 
        self.setControlEvents()
        self.searchString = []


    def extractRows(self, rowId):
        """Returns 3 rows prior to rowId (see self.db.getRows... statement)
        Return: A dict with two keys containing the complete rows ('fullrows':)
        and the rows for the preview table ('adjecentrows':)"""
        rows = self.db.getRows(f'specimen WHERE id <= {rowId} ', limit=3, sortColumn='id DESC')
        headers = ['id', 'spid', 'catalognumber', 'multispecimen', 'taxonfullname', 'taxonname', 'taxonnameid',
                   'taxonspid',
                   'highertaxonname', 'typestatusname', 'typestatusid', 'georegionname', 'georegionid',
                   'storagefullname',
                   'storagename', 'storageid', 'preptypename', 'preptypeid', 'notes', 'institutionid', 'collectionid',
                   'username', 'userid', 'recorddatetime', 'exported', 'exportdatetime', 'exportuserid']
        specimenList = [[row for row in line] for line in rows]
        # print('init rows :', rows)
        # Code block below takes the rows returned and
        # operationalRows = []
        tempDicts = [] #full rows needed to populate the form
        adjecentRows = [] #the curated rows needed to populate the table
        for row in specimenList:
            specimenDict = dict(zip(headers, row))
            # print('full row:-', specimenDict)
            tempDicts.append(specimenDict)
            tempAdjecent = []
            for k in self.operationalHeads:
                res = specimenDict[k]
                # print('Adjecent rows item: ', res)
                tempAdjecent.append(res)
            adjecentRows.append(tempAdjecent)
        rowsExtracted = {'fullrows': tempDicts, 'adjecentrows': adjecentRows}
        return rowsExtracted

    def previousRows3(self, **kwargs):
        #Get previous three records. Kwargs expects an Id number (id=[integer]) or no keyword arg.
        if kwargs:
            filter = f"specimen WHERE id <= {kwargs['id']}"
            rows = self.db.getRows(filter, limit=3, sortColumn='id DESC')
        else:
            rows = self.db.getRows('specimen', limit=3, sortColumn='id DESC')
        self.previousRecords = [[row for row in line] for line in rows]
        return self.previousRecords

    def main(self):
        if self.currentRecordId:
            overviewRows = self.extractRows(self.currentRecordId)
        elif self.maxRow:
            overviewRows = self.extractRows(self.maxRow)
        else:
            overviewRows = {'adjecentrows': [[],[],[]]}
        tblRows = list(overviewRows['adjecentrows'])
        self.window['tblPrevious'].update(values = tblRows)

        while True:
            event, values = self.window.Read()
                # timeout=700, timeout_key='_timeout')

            # Checking field events as switch construct
            if event is None: break  # Empty event indicates user closing window
            # print("-event-", event)
            if event == 'txtStorage':
                self.searchString.append(values[event])
                # If more than 3 characters entered: 
                if len(self.searchString) >= 3:
                    # Get currently entered key strokes

                    keyStrokes = self.searchString.pop()

                    self.autoStorage.Show()

                    # Fetch storage location record from database based on user interactions with autosuggest popup window 
                    selectedStorage = self.autoStorage.captureSuggestion(keyStrokes)
                    
                    # Set storage fields using record retrieved
                    if selectedStorage is not None:
                        # Set specimen record storage fields 
                        self.collobj.setStorageFieldsFromModel(selectedStorage)

                        # Update UI to indicate selected storage record  
                        self.window['txtStorageFullname'].update(selectedStorage.fullName)
                        self.window['txtStorage'].update(selectedStorage.name)
                        
                        # Move focus to next field (PrepTypes list). This is necessary due to all keys being captured
                        # for the autoSuggest/capture_suggestion function.
                        self.window['cbxPrepType'].set_focus()

            if event == 'cbxPrepType':
                self.collobj.setPrepTypeFields(self.window[event].widget.current())
                self.window['cbxTypeStatus'].set_focus()

            # if event == 'cbxHigherTaxon':
            #    pass

            if event == 'cbxTypeStatus':
                # TypeStatus is preloaded in the Class
                self.collobj.setTypeStatusFields(self.window[event].widget.current())
                self.collobj.typeStatusName = self.window['cbxTypeStatus'].get()
                self.window['txtNotes'].set_focus()

            if event == 'txtNotes_Edit':
                self.collobj.notes = values['txtNotes']
                self.window['chkMultiSpecimen'].set_focus()

            if event == '_Tab':
                self.collobj.notes = values['txtNotes']
                # self.window['chkMultiSpecimen'].set_focus()

            if event == 'chkMultiSpecimen_Enter':
                # This event is only triggered by being in the checkbox element
                # and pressing Enter.
                check = self.window['chkMultiSpecimen'].Get()
                self.collobj.multiSpecimen = values['chkMultiSpecimen']
                self.window['cbxGeoRegion'].set_focus()

            if event == 'chkMultiSpecimen_Edit':
                self.collobj.multiSpecimen = values['chkMultiSpecimen']

            if event == 'cbxGeoRegion':
                self.collobj.setGeoRegionFields(self.window[event].widget.current())
                self.window['inpTaxonName'].set_focus()

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
                        # Set specimen record taxon name fields 
                        self.collobj.setTaxonNameFieldsFromModel(selectedTaxonName)
                        temp = str(selectedTaxonName).split(' ')
                        prenote = temp[-2:]
                        if prenote[0] == '=':
                            prenote.pop(0)
                        self.notes = ' '.join(prenote)
                        # Update UI to indicate selected taxon name record  
                        self.window['inpTaxonName'].update(selectedTaxonName.fullName)
                        
                        # Move focus further to next field (Barcode textbox)
                        self.window['txtCatalogNumber'].set_focus()
                        # window['cbxTaxonName'].update(set_to_index=[0], scroll_to_index=0)

            if event == 'txtCatalogNumber':
                self.collobj.catalogNumber = values[event]

            if event == 'txtCatalogNumber_Edit':
                self.collobj.catalogNumber = values['txtCatalogNumber']

            if event == "txtCatalogNumber_Enter":
                self.collobj.catalogNumber = values['txtCatalogNumber']
                self.window['btnSave'].set_focus()

            if event == 'btnClear':
                # Clear all clearable fields as defined in list 'clearingFields'
                self.clearForm()

            if event == 'btnBack':
                # Fetch previous specimen record data on basis of current record ID, if any
                record = self.collobj.loadPrevious(self.collobj.id) 
                if record:
                    # If not empty, set form fields
                    self.fillFormFields(record)
                else:
                    # Indicate no further records
                    self.window['lblRecordEnd'].update(visible=False)

            if event == 'btnForward':
                # Fetch next specimen record data on basis of current record ID, if any
                record = self.collobj.loadNext(self.collobj.id)  
                if record:
                    # If not empty, set form fields
                    self.fillFormFields(record)
                else:
                    # Indicate no further records
                    self.window['lblRecordEnd'].update(visible=False)

            # if event == 'btnClear':
            #     for key in self.clearingList:
            #         self.window[key].update('')
            #
            #     self.window['lblExport'].update(visible=False)
            #     self.window['lblRecordEnd'].update(visible=False)

            if event == 'btnExport':
                export_result = dx.exportSpecimens('xlsx')
                self.window['lblExport'].update(export_result, visible=True)

            if event == 'btnDismiss':
                self.window['lblExport'].update(visible=False)
                self.window['lblRecordEnd'].update(visible=False)

            if event == '_timeout':
                #DEprecated
                recordIDnow = self.window['txtRecordID'].get()
                if recordIDnow:
                    newAdjecents = self.extractRows(recordIDnow)
                    self.window['tblPrevious'].update(values=newAdjecents['adjecentrows'])


            if event == sg.WINDOW_CLOSED:
                break

            # Save form 
            if event == 'btnSave' or event == 'btnSave_Enter':
                # save specimen and get its id
                if len(self.notes) > 5: # test to see if remark (verbatim note) was passed from autosuggest.
                    self.collobj.notes = self.window['txtNotes'].Get()+' | '+self.notes
                else:
                    self.collobj.notes = self.window['txtNotes'].Get()
                specimenRecord = self.collobj.save()
                # print(f"-SAVING from button Save-\n {specimenRecord}")
                self.clearNonStickyFields(values)

                # Create a new specimen instance and add previous id to it 
                self.collobj = specimen.specimen(self.collectionId) 
                
                # Transfer data in sticky fields to new record:
                self.setRecordFields('specimen', specimenRecord, True)

                self.window['txtCatalogNumber'].set_focus()
                recid = self.window['txtRecordID'].Get()

            if event == 'tblPrevious':
                tblVals = values['tblPrevious']
                # data_selected = [tblVals[row] for row in values[event]]
                # print("################# data selected = ", data_selected)
                currentRowId = self.window['txtRecordID'].get()
                if currentRowId:
                    rowsDict = self.extractRows(currentRowId)
                    self.window['tblPrevious'].update(rowsDict['adjecentrows'])
                else:
                    selected_index = values['tblPrevious'][0]
                chosenRows= overviewRows['fullrows']
                selectedRow = chosenRows[selected_index]
                self.fillFormFields(selectedRow)
                newAdjecents = self.extractRows(selectedRow['id'])
                newAdjecents = newAdjecents['adjecentrows']
                self.window['tblPrevious'].update(values=newAdjecents)
                # import time
                # print('sleeeeping for 3')
                # time.sleep(3)
            #     if self.window['txtRecordID'].get():
            #         currentRecordId = self.window['txtRecordID'].get()
            #         print(f'THE currend REC ID IS .{currentRecordId}.')
            #     else:
            #         currentRecordId = self.maxRow
            #     self.previousRecords = self.extractRows(currentRecordId)
            #     #Extracting the full rows from the returned dictionary {fullrows: , adjacentrows: }
            #     fullRows = self.previousRecords['fullrows']
            #
            #     selected_index = values['tblPrevious'][0]
            #     selected_row = self.previousRecords[selected_index]
            #     print(self.headers,'\n',selected_row)
            #     rowDict = dict(zip(self.operationalHeads, selected_row))
            #     print('THE adjacent rowdict::', rowDict)
            #     self.fillFormFields(rowDict)

        self.window.close()

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
        self.collobj.setStorageFields(self.db.getRowOnId(tableName, record['storageid']))
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
        self.window['txtStorage'].update(record['storagename'])
        self.window['txtStorageFullname'].update(record['storagefullname'])
        self.window['cbxPrepType'].update(record['preptypename'])
        # self.window['cbxHigherTaxon'].update('')
        self.window['cbxTypeStatus'].update(record['typestatusname'])
        self.window['txtNotes'].update(record['notes'])
        if record['multispecimen'] == 'True': 
            self.multiSpecimen = True 
            self.window['chkMultiSpecimen'].update(True)
        else: 
            self.multiSpecimen = False
            self.window['chkMultiSpecimen'].update(False)
        # self.window['chkMultiSpecimen'].update(multiSpecimen)
        self.window['cbxGeoRegion'].update(record['georegionname'])
        self.window['inpTaxonName'].update(record['taxonfullname'])
        self.window['txtCatalogNumber'].update(record['catalognumber'])

    def clearNonStickyFields(self, values):
        """
        Function for clearing all fields that are non-sticky 
        """
        for key in self.nonStickyFields:
            field = self.window[key]
            field.update('')

    def clearForm(self):
        """
        Function for clearing all fields listed in clearing list 
        """ 
        for key in self.clearingList:
            self.window[key].update('')
        self.window['lblExport'].update(visible=False)
        self.window['lblRecordEnd'].update(visible=False)
        self.searchString = []
