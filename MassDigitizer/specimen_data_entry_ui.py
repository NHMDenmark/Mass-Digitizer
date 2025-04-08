# -*- coding: utf-8 -*-

"""
Created on Fri Jan 24 2025 11:12:00 
@author: Fedor Alexander Steeman NHMD;

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
import time
import traceback
from pathlib import Path

# PySide6 imports
from PySide6.QtWidgets import QLineEdit, QComboBox, QRadioButton, QCheckBox, QMessageBox
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, QFile, QStandardPaths, QStringListModel
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import QCompleter
from PySide6.QtUiTools import QUiLoader

# Internal dependencies
import util
import data_access
import global_settings as gs
from models import specimen
from models import recordset
from models import collection as coll

class SpecimenDataEntryUI(QMainWindow):

    def __init__(self, collection_id):
        """
        Constructor for the SpecimenDataEntryUI class.
        """
        super(SpecimenDataEntryUI, self).__init__()

        # Set class variables
        self.collection_id = collection_id
        self.collection = coll.Collection(collection_id)
        self.MSOterm = 'Multiple specimens on one object'
        self.MOSterm = 'One specimen on multiple objects'
        self.db = data_access.DataAccess(gs.databaseName)  # Instantiate database access module
        self.collobj = specimen.Specimen(collection_id)  # Create blank specimen record instance

        # Input field lists defining: Tabbing order, focus indicator, what fields to be cleared, and what fields are not 'sticky' i.e. not carrying their value over to the next record after saving current one 
        #self.inputFieldList  = ['inpStorage', 'cbxPrepType', 'cbxTypeStatus', 'cbxGeoRegion', 'inpTaxonName', 'inpTaxonNumber', 'chkDamage', 'chkSpecimenObscured', 'chkLabelObscured', 'radRadioSSO', 'radRadioMSO', 'radRadioMOS', 'inpContainerName', 'inpNotes', 'inpCatalogNumber', 'btnSave']
        #self.focusIconList   = ['inrStorage', 'inrPrepType', 'inrTypeStatus', 'inrGeoRegion', 'inrTaxonName', 'inrTaxonNumber', 'inrDamage', 'inrSpecimenObscured', 'inrLabelObscured', 'inrRadioSSO', 'inrRadioMSO', 'inrRadioMOS', 'inrContainerName', 'inrNotes', 'inrCatalogNumber', 'inrSave']
        self.clearingList    = ['inpStorage', 'cbxPrepType', 'cbxTypeStatus', 'cbxGeoRegion', 'inpTaxonName', 'inpTaxonNumber', 'chkDamage', 'chkSpecimenObscured', 'chkLabelObscured','inpContainerName', 'inpCatalogNumber','txtRecordID', 'txtStorageFullname', 'inpNotes']
        self.nonStickyFields = ['inpCatalogNumber', 'txtRecordID', 'chkDamage', 'chkSpecimenObscured', 'chkLabelObscured', 'inpNotes']
        self.sessionMode     = 'Default'
        
        # Load UI and setup connections
        self.load_ui()
        self.setControlEvents()
        self.setup_form(collection_id)

        self.collectionId = collection_id  # Set collection Id
        self.collection = coll.Collection(collection_id)
        self.window = None  # Create class level instance of window object
        self.db = data_access.DataAccess(gs.databaseName)  # Instantiate database access module
        self.collobj = specimen.Specimen(collection_id)  # Create blank specimen record instance

        # Create recordset of last 3 saved records for the initial preview table
        self.tableHeaders = ['id', 'catalognumber', 'taxonfullname', 'containertype', 'georegionname','storagename'] 
        self.recordSet = recordset.RecordSet(collection_id, 3,specimen_id=self.collobj.id) 

         # Load data
        self.load_comboboxes()
        self.load_previous_records()

        # Set image resource
        documents_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        image_path = os.path.join(documents_path, "DaSSCo", "img", "Warning_LinkedRecord.png")
        self.ui.imgWarningLinkedRecord.setPixmap(QPixmap(image_path))

        # Set metadata
        self.ui.txtUserName.setText(gs.userName)
        self.ui.txtCollection.setText(self.collection.name)     
        self.ui.txtInstitution.setText(gs.institutionName)
        self.ui.txtVersionNr.setText(util.getVersionNumber())

        # Create QCompleter for inpStorage
        self.storage_completer = QCompleter()
        self.storage_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.storage_completer.setFilterMode(Qt.MatchContains)
        self.storage_completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.ui.inpStorage.setCompleter(self.storage_completer)
        self.ui.inpStorage.textChanged.connect(self.update_storage_completer)  

        # Create QCompleter for inpTaxonName
        self.taxonname_completer = QCompleter()
        self.taxonname_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.taxonname_completer.setFilterMode(Qt.MatchContains)
        self.ui.inpTaxonName.setCompleter(self.taxonname_completer)
        self.ui.inpTaxonName.textChanged.connect(self.update_taxonname_completer)
        
        # Start up interface and center window
        self.show()
        self.center_screen() 
        
    def load_comboboxes(self):
        """
        Load comboboxes with data from the database.
        """
        
        self.ui.cbxPrepType.addItem('-please select-', -1)
        for item in self.collobj.prepTypes:
            self.ui.cbxPrepType.addItem(str(item[2]), item[0])
        
        self.ui.cbxTypeStatus.addItem('-please select-', -1)
        for item in self.collobj.typeStatuses:
            self.ui.cbxTypeStatus.addItem(str(item[2]), item[0])
        
        self.ui.cbxGeoRegion.addItem('-please select-', -1)
        for item in self.collobj.geoRegions:
            self.ui.cbxGeoRegion.addItem(str(item[1]), item[0])

    def load_previous_records(self):
        """
        Load previous records into the tblPrevious table widget.
        """

        # Clear existing rows
        self.ui.tblPrevious.setRowCount(0)

        # Iterate over the records in the recordSet
        for record in self.recordSet.records:
            row_position = self.ui.tblPrevious.rowCount()
            self.ui.tblPrevious.insertRow(row_position)

            # Add only the specified columns to the table
            for column_index, column_header in enumerate(self.tableHeaders):
                value = record[column_header]  # Access the value using the column header
                self.ui.tblPrevious.setItem(row_position, column_index, QTableWidgetItem(str(value)))

        # Adjust row height and column width to fit contents
        self.ui.tblPrevious.resizeRowsToContents()
        self.ui.tblPrevious.resizeColumnsToContents()

    def load_ui(self):
        """
        Load the UI from the .ui file and customize selected widgets.
        """
        loader = QUiLoader()
        ui_path = util.resourcePath("ui/specimendataentry.ui")
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set window properties
        imgPath = str(Path(util.getUserPath()).joinpath(f'img/DaSCCo-logo.png'))
        self.setWindowIcon(QIcon(imgPath))
        self.setWindowTitle("DaSSCo Mass Digitization App")

        # Set font for table headers
        header_font = QFont("Arial", 12)
        self.ui.tblPrevious.horizontalHeader().setFont(header_font)
        self.ui.tblPrevious.verticalHeader().setFont(header_font)

        # Set column widths for previous records table
        self.ui.tblPrevious.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.tblPrevious.setColumnWidth(0, 50)  # Set width for id column
        self.ui.tblPrevious.setColumnWidth(1, 150)  # Set width for catalognr column
        self.ui.tblPrevious.setColumnWidth(2, 200)  # Set width for taxonfullname column
        self.ui.tblPrevious.setColumnWidth(3, 200)  # Set width for containertype column
        self.ui.tblPrevious.setColumnWidth(4, 200)  # Set width for georegionname column
        self.ui.tblPrevious.setColumnWidth(5, 200)  # Set width for storagename column

    def setup_form(self, collection_id):
        """
        Setup the specimen data entry form.
        """
        util.logger.info('*** Specimen data entry setup ***')

        self.ui.txtUserName.setText(gs.userName)
        collection = self.db.getRowOnId('collection', collection_id)
        if collection is not None:
            self.ui.txtCollection.setText(collection[2])
            institution = self.db.getRowOnId('institution', collection[3])
            self.ui.txtInstitution.setText(institution[2])

        if self.collection.useTaxonNumbers:
            self.ui.lblTaxonNumber.setVisible(True)
            self.ui.inpTaxonNumber.setVisible(True)
        else:
            self.ui.lblTaxonNumber.setVisible(False)
            self.ui.inpTaxonNumber.setVisible(False)
        
        self.updateRecordCount()

    def setControlEvents(self):
        """
        Set specific control events for the specimen data entry form.
        To ensure rapid form flow, each input field's edit event forwards focus to the next field on the form. 
        Upon each edit, the internal state of the collection object data needs to be updated immediately.
        Buttons for saving and navigations are connected to specific functions.
        """

        # Ensure next input receives focus upon edit 
        for line_edit in self.findChildren(QLineEdit): 
            line_edit.returnPressed.connect(self.focusNextChild)

        for combo_box in self.findChildren(QComboBox):
            combo_box.currentIndexChanged.connect(self.focusNextChild)
        
        for radio_button in self.findChildren(QRadioButton):
            radio_button.toggled.connect(self.on_containerTypeToggle)

        # Connect input field signals to data update functions
        self.ui.inpStorage.returnPressed.connect(self.on_inpStorage_return_pressed)
        self.ui.cbxPrepType.currentIndexChanged.connect(self.on_cbxPrepType_currentIndexChanged)
        self.ui.cbxTypeStatus.currentIndexChanged.connect(self.on_cbxTypeStatus_currentIndexChanged)
        self.ui.cbxGeoRegion.currentIndexChanged.connect(self.on_cbxGeoRegion_currentIndexChanged)
        self.ui.inpTaxonName.returnPressed.connect(self.on_inpTaxonName_return_pressed)
        self.ui.chkDamage.clicked.connect(self.on_chkDamage_clicked)
        self.ui.chkSpecimenObscured.clicked.connect(self.on_chkSpecimenObscured_clicked)
        self.ui.chkLabelObscured.clicked.connect(self.on_chkLabelObscured_clicked)
        self.ui.radRadioSSO.toggled.connect(self.on_containerTypeToggle)
        self.ui.radRadioMOS.toggled.connect(self.on_containerTypeToggle)
        self.ui.radRadioMSO.toggled.connect(self.on_containerTypeToggle)
        self.ui.inpContainerName.returnPressed.connect(self.on_container_name_return_pressed)
        self.ui.inpNotes.returnPressed.connect(self.on_notes_return_pressed)        
        self.ui.inpCatalogNumber.returnPressed.connect(self.on_catalog_number_return_pressed)
        self.ui.inpCatalogNumber.textChanged.connect(self.on_catalog_number_text_changed)      
        self.ui.inpTaxonNumber.returnPressed.connect(self.lookup_taxon_number)
        self.ui.inpTaxonNumber.textChanged.connect(self.lookup_taxon_number)
        
        # Connect buttons to specific action functions
        self.ui.btnSave.clicked.connect(self.on_save_clicked)
        self.ui.btnBack.clicked.connect(self.on_back_clicked)
        self.ui.btnForward.clicked.connect(self.on_forward_clicked)
        self.ui.btnClear.clicked.connect(self.clearForm)

    def on_save_clicked(self): self.saveForm()

    def on_inpStorage_return_pressed(self): 
        """
        Set storage fields from storage input field and update the storage full name field.
        """
        storage_name_input = self.ui.inpStorage.text()
        self.ui.txtStorageFullname.setText(storage_name_input)
        storage_record = self.getStorageRecord()
        if storage_record:
            self.collobj.setStorageFieldsFromRecord(storage_record)
        else: 
            self.collobj.storageName = storage_name_input
            self.collobj.storageFullName = storage_name_input
            self.collobj.storageId = 0
        self.ui.txtStorageFullname.setText(self.collobj.storageFullName)

    def on_cbxPrepType_currentIndexChanged(self): self.collobj.setPrepTypeFields(self.ui.cbxPrepType.currentIndex() - 1)

    def on_cbxTypeStatus_currentIndexChanged(self): self.collobj.setTypeStatusFields(self.ui.cbxTypeStatus.currentIndex() - 1)

    def on_cbxGeoRegion_currentIndexChanged(self): self.collobj.setGeoRegionFields(self.ui.cbxGeoRegion.currentIndex() - 1)

    def on_inpTaxonName_return_pressed(self): 
        """
        Set taxon name fields from taxon name input field.
        """
        taxon_name_input = self.ui.inpTaxonName.text()
        record = self.getTaxonNameRecord(taxon_name_input)
        if record:
            self.collobj.setTaxonNameFieldsFromRecord(record)
        else: 
            self.collobj.taxonName = taxon_name_input
            self.collobj.taxonFullName = taxon_name_input
            self.collobj.taxonNameId = 0
        self.setTxtTaxonFullname(self.collobj.taxonFullName)

    def on_chkDamage_clicked(self): 
        needsrepair = self.ui.chkDamage.isChecked()
        if needsrepair: 
            self.collobj.objectCondition = "Needs repair"
        else: 
            self.collobj.objectCondition = ""
        self.ui.chkSpecimenObscured.setFocus()
        
    def on_chkSpecimenObscured_clicked(self):
        self.collobj.specimenObscured = self.ui.chkSpecimenObscured.isChecked()
        self.ui.chkLabelObscured.setFocus()

    def on_chkLabelObscured_clicked(self):
        self.collobj.labelObscured = self.ui.chkSpecimenObscured.isChecked()  
        self.ui.radRadioSSO.setFocus()
        
    def on_containerTypeToggle(self, checked):
        """
        Set container type controls events: 
            - Multi objects require a randomized container id prefixed with type. 
              And a user Warning needs to displayed. 
            - A single specimen object does not need a container id
            - Save changes to collection object for saving record data 
        """
        
        if checked:
            if self.sender() == self.ui.radRadioSSO:
                # A single specimen object does not require a container name
                self.ui.inpContainerName.setText('')
                self.ui.inpContainerName.setEnabled(False)
                self.ui.imgWarningLinkedRecord.setVisible(False)
                self.collobj.containername = ''
                self.collobj.containertype = ''
            elif self.sender() == self.ui.radRadioMOS or self.sender() == self.ui.radRadioMSO:
                # A multi specimen object requires a container name and a warning to the user
                containerNumber = util.getRandomNumberString()
                containerType = ''
                if self.sender() == self.ui.radRadioMOS:
                    containerType = 'MOS'
                    self.collobj.containertype = self.MOSterm
                elif self.sender() == self.ui.radRadioMSO:
                    containerType = 'MSO'
                    self.collobj.containertype = self.MSOterm
                newContainerName = containerType + str(containerNumber)
                self.collobj.containername = newContainerName

                self.ui.inpContainerName.setText(newContainerName)
                self.ui.inpContainerName.setEnabled(True)
                self.ui.imgWarningLinkedRecord.setVisible(True)

            self.ui.inpNotes.setFocus()
    
    def on_container_name_return_pressed(self):self.collobj.containername = self.ui.inpContainerName.text()

    def on_notes_return_pressed(self): 
        self.collobj.notes = self.ui.inpNotes.text()

    def on_catalog_number_return_pressed(self): 
        self.collobj.catalogNumber = self.ui.inpCatalogNumber.text()
        self.saveForm()

        util.logger.info(f'New collection object: {str(self.collobj)}')
        pass

    def on_catalog_number_text_changed(self): self.collobj.catalogNumber = self.ui.inpCatalogNumber.text()

    def lookup_taxon_number(self):
        """Lookup taxon number in database and set taxon name fields accordingly."""
        taxon_nr_input = self.ui.inpTaxonNumber.text()
        if len(taxon_nr_input) > 1:
            #self.collobj.taxonNumber = self.ui.inpTaxonNumber.text()
            record = self.getTaxonNameRecordOnNumber(taxon_nr_input)
            if record:
                self.collobj.setTaxonNameFieldsFromRecord(record)            
                self.ui.inpTaxonName.setText(self.collobj.taxonFullName)
            else: 
                self.collobj.taxonName = ''
                self.collobj.taxonFullName = ''
                self.collobj.taxonNameId = 0            
                self.ui.inpTaxonName.setText('')

    def on_back_clicked(self):
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
            self.load_form(record)

        # Fill form fields 
        self.fillFormFields()

        # Reset focus back to first field (Storage)
        self.ui.inpStorage.setFocus()

    def on_forward_clicked(self):
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
            self.load_form(record)

        # Fill form fields 
        self.fillFormFields()
        
        # Reset focus back to first field (Storage)
        self.ui.inpStorage.setFocus()

    def load_form(self, record):
        """Load form with data from record."""
        self.collobj.setFields(record)
        self.fillFormFields()

        # Reload recordset and repopulate table of adjacent records
        self.recordSet.reload(record)
        self.load_previous_records()

    def updateRecordCount(self):
        """
        Simple method for retrieving and displaying record count
        """
        # Update record number counter 
        filter = {'institutionid':f'={self.collection.institutionId}','collectionid':f'={self.collection.id}'}
        records = self.db.getRowsOnFilters('specimen', filters=filter, limit=9999)
        if records:
            specimenCount = len(records)
        else: 
            specimenCount = 0
        self.ui.txtNumberCounter.setText(str(specimenCount))

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

                # Remember id of record just saved and prepare for blank record
                previousRecordId = savedRecord['id'] 

                # Refresh adjacent record set
                self.recordSet.reload(savedRecord)

                self.recordSet.getAdjacentRecordList(self.tableHeaders)
                self.load_previous_records()

                result = "Successfully saved specimen record."

                util.logger.info(f'{result} : {previousRecordId} - {savedRecord}')

                # If so, prepare for new blank record
                if newRecord:
                    # Create a new, blank specimen record (id pre-set to 0)
                    self.collobj = specimen.Specimen(self.collectionId)                    

                    # Transfer data in sticky fields to new record:
                    self.setSpecimenFields() 
                    self.fillFormFields()
                    
                    # Prepare form for next new record
                    self.clearNonStickyFields()
            else:
                result = 'validation error'

        except Exception as e:
            errorMessage = f"Error occurred attempting to save specimen: {e}"
            traceBack = traceback.format_exc()
            util.logger.error(errorMessage)
            self.show_error_popup(f'{e} \n\n {traceBack}', title='Error handle storage input')
            result = errorMessage

        self.ui.inpCatalogNumber.setFocus()

        self.updateRecordCount()

        util.logger.info(f'{result}')
                         
        return result

    def setSpecimenFields(self, stickyFieldsOnly=True):
        """
        Method for synchronizing specimen data object instance (Model) with form input fields (View).
        CONTRACT
            stickyFieldsOnly (Boolean) : Indication of only sticky fields should be synchronized usually in case of a new blank record
        """

        # Set specimen object instance fields from input form
        self.collobj.setStorageFieldsFromRecord(self.getStorageRecord())
        self.collobj.setPrepTypeFields(self.ui.cbxPrepType.currentIndex() - 1)
        self.collobj.setTypeStatusFields(self.ui.cbxTypeStatus.currentIndex() - 1)
        self.collobj.notes = self.ui.inpNotes.text()
        self.collobj.containername = self.ui.inpContainerName.text()
        self.collobj.containertype = self.getContainerTypeFromInput()
        self.collobj.setGeoRegionFields(self.ui.cbxGeoRegion.currentIndex() - 1)
        taxonFullName = self.ui.inpTaxonName.text()
        taxonFullName = taxonFullName.rstrip()
        if self.collection.useTaxonNumbers:
            self.collobj.taxonNumber = self.ui.inpTaxonNumber.text()
        self.collobj.setTaxonNameFields(self.getTaxonNameRecord(taxonFullName))
        pass
    
    def clearNonStickyFields(self):
        """
        Function for clearing all fields that are non-sticky
        """        
        self.clearForm(self.nonStickyFields)

    def clearForm(self, fieldList=None):
        """
        Function for clearing all fields listed in clearing list and setting up for a blank record
        """
                
        if not fieldList: fieldList = self.clearingList

        # Clear fields defined in clearing list
        for key in fieldList:
            textfield = self.ui.findChild(QLineEdit, key)
            if textfield: textfield.setText('')
            listfield = self.ui.findChild(QComboBox, key)
            if listfield: listfield.setCurrentIndex(0)
            checkfield = self.ui.findChild(QCheckBox, key)
            if checkfield: checkfield.setChecked(False)

        if 'inpContainerName' in fieldList:
            self.ui.radRadioSSO.setChecked(True)

        # If existing record, highlight record id
        if self.collobj.id > 0:
            self.ui.txtRecordID.setStyleSheet("QLabel { background-color: yellow }")
        else:
            self.ui.txtRecordID.setStyleSheet("")

        # Reset focus on the storage field
        self.ui.inpStorage.setFocus()   

    def getStorageRecord(self):
        """
        Retrieve storage record based on storage input field contents.
        Search is to be done on fullname since identical atomic values can occur across the storage tree with different parentage.
        """
        storageFullName = self.ui.txtStorageFullname.text()
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

    def getContainerTypeFromInput(self):
        """
        Get container type based on what radio button was selected
        """
        containerType = '' # 'Single Specimen Object'

        if self.ui.radRadioMSO.isChecked():
            containerType = self.MSOterm
        elif self.ui.radRadioMOS.isChecked():
            containerType = self.MOSterm

        return containerType

    def getTaxonNameRecord(self, taxonFullName):
        """
        Retrieve taxon name record based on taxon name input field contents.
        Search is to be done on taxon fullname and taxon tree definition derived from collection.
        """
        # Replace apostrophes with double quotes for SQL query
        taxonFullName = taxonFullName.replace("'", "''")

        taxonRecords = self.db.getRowsOnFilters('taxonname', {'fullname': f'="{taxonFullName}"', 'institutionid': f'={self.collection.institutionId}', 'treedefid': f'={self.collection.taxonTreeDefId}'}, 1)
        if len(taxonRecords) > 0:
            taxonRecord = taxonRecords[0]
        else:
            taxonRecord = None
        return taxonRecord
    
    def getTaxonNameRecordOnNumber(self, taxonNumber):
        """
        Retrieve taxon name record based on taxon number input field contents.
        Search is to be done on taxon number and taxon tree definition derived from collection.
        """

        taxonRecords = self.db.getRowsOnFilters('taxonname', {'idnumber': f'="{taxonNumber}"', 'institutionid': f'={self.collection.institutionId}', 'treedefid': f'={self.collection.taxonTreeDefId}'}, 1)
        if len(taxonRecords) > 0:
            taxonRecord = taxonRecords[0]
        else:
            taxonRecord = None
        return taxonRecord

    def fillFormFields(self):
        """
        Function for setting form fields from specimen data record
        """        
        record = self.collobj.getFieldsAsDict()

        self.ui.txtRecordID.setText(record.get('id', '-new record-'))
        if record.get('id') == '0': self.ui.txtRecordID.setText('-new record-')
        self.ui.inpStorage.setText(record.get('storagefullname', ''))
        self.ui.txtStorageFullname.setText(record.get('storagefullname', ''))
        self.ui.cbxPrepType.setCurrentText(record.get('preptypename', ''))
        self.ui.cbxTypeStatus.setCurrentText(record.get('typestatusname', ''))

        if record.get('objectcondition') == 'Needs repair':
            self.ui.chkDamage.setChecked(True)
        else:
            self.ui.chkDamage.setChecked(False)
        self.ui.chkSpecimenObscured.setChecked(util.str_to_bool(record.get('specimenobscured', 'False')))
        self.ui.chkLabelObscured.setChecked(util.str_to_bool(record.get('labelobscured', 'False')))

        self.ui.inpNotes.setText(record.get('notes', ''))

        self.setContainerFields(record)

        self.ui.cbxGeoRegion.setCurrentText(record.get('georegionname', ''))
       
        taxonfullname = record.get('taxonfullname', '-no taxon selected-')
        self.setTxtTaxonFullname(taxonfullname)

        if self.collection.useTaxonNumbers:
            self.ui.inpTaxonNumber.setText(record.get('taxonnumber', ''))
        self.ui.inpCatalogNumber.setText(record.get('catalognumber', ''))

        self.ui.txtRecordID.setStyleSheet("")

    def setTxtTaxonFullname(self, taxonfullname):
        if taxonfullname != '':
            taxonfamilyname = self.collobj.searchParentTaxon(taxonfullname, 140, self.collection.taxonTreeDefId)
            self.ui.inpTaxonName.setText(taxonfullname)
            self.ui.txtTaxonFullname.setText(taxonfullname + ' (' + taxonfamilyname + ')')
        else: 
            self.ui.txtTaxonFullname.setText('-no taxon selected-')
    
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
                self.ui.radRadioMSO.setChecked(True) # Set MSO radiobutton 
                self.ui.imgWarningLinkedRecord.setVisible(True)
            elif containerType == self.MOSterm:
                self.ui.radRadioMOS.setChecked(True) # Set MOS radiobutton
                self.ui.imgWarningLinkedRecord.setVisible(True)
            else:
                self.ui.lblError.setText('Something went wrong!')
                self.ui.lblError.setVisible=True
            
            self.ui.inpContainerName.setText(containerName)
            self.ui.inpContainerName.setEnabled(True)
        else:
            # No container name set; single specimen assumed
            self.ui.radRadioSSO.setChecked(True) # Set SSO radiobutton        
            self.ui.inpContainerName.setText('') # Clear container name input field 
            self.ui.inpContainerName.setEnabled(False) # Disable container name input field 
            self.ui.imgWarningLinkedRecord.setVisible(False) # Hide linked record warning

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
        self.show_error_popup(validationMessage)

    def center_screen(self):
        # Get the existing QApplication instance
        app = QApplication.instance()

        # Center the window on the screen
        screen = app.primaryScreen()
        center = screen.availableGeometry().center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        pass

    def show_error_popup(self, error_message, title='Error'):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(error_message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def update_storage_completer(self, keyStrokes):
        """
        Update the storage input field with suggestions based on the user's key strokes.

        Parameters:
        keyStrokes (str): The current text input by the user in the storage input field.
        """

        if isinstance(keyStrokes, str) and len(keyStrokes) >= 3:
            fields = {'fullname': f'LIKE "%{keyStrokes.lower()}%"', 'collectionid': f'={self.collection_id}'}
            rows = self.db.getRowsOnFilters('storage', fields, 50)
            suggestions = []
            for row in rows:
                fullname = row['fullname']
                # parts = fullname.split('|')
                # if len(parts) > 2:
                #     shortened_fullname = '|'.join(parts[2:]).strip()
                #     suggestions.append(shortened_fullname)
                # else:
                suggestions.append(fullname.strip())
            self.storage_completer.setModel(QStringListModel(suggestions))
        else:
            self.storage_completer.setModel(QStringListModel([]))

    def update_taxonname_completer(self, keyStrokes):
        """
        Update the taxon name input field with suggestions based on the user's key strokes.

        Parameters:
        keyStrokes (str): The current text input by the user in the taxon name input field.
        """
        if isinstance(keyStrokes, str) and len(keyStrokes) >= 3:
            # Format the search term with double quotation marks to work witch FTS MATCH
            sanitized_input = keyStrokes.replace('.', '"."')  # Escapes periods in FTS5
            sanitized_input = sanitized_input.replace('-', '"-"')  # Escapes dashes in FTS5
            sanitized_input = sanitized_input.replace('(', '"("')  # Escapes parenthesis open in FTS5
            sanitized_input = sanitized_input.replace(')', '")"')  # Escapes parenthesis closed in FTS5
            sanitized_input = sanitized_input.replace(',', '","')  # Escapes comma in FTS5
            sanitized_input = sanitized_input.replace('&', '"&"')  # Escapes obelisk in FTS5
            search_term = f'{sanitized_input}*'
            
            sqlString = f"""SELECT * FROM taxonname WHERE id IN (SELECT id FROM taxonname_fts  
                            WHERE fullname MATCH '{search_term}' AND institutionid = {self.collection.institutionId} 
                            AND taxontreedefid = {self.collection.taxonTreeDefId} LIMIT 200 );"""
            try:
                rows = self.db.executeSqlStatement(sqlString)
                suggestions = [row['fullname'].strip() for row in rows]
                self.taxonname_completer.setModel(QStringListModel(suggestions))
            except Exception as e:
                util.logger.error(f"Error occurred while fetching taxon name suggestions: {e}")
                util.logger.error(f"SQL string: {sqlString}")
                util.logger.error(f"Error stack: {e.__traceback__}")
                self.show_error_popup(f"Error occurred while fetching taxon name suggestions: {e}")
                self.taxonname_completer.setModel(QStringListModel([]))
        else:
            self.taxonname_completer.setModel(QStringListModel([]))
    

def main():
    app = QApplication(sys.argv)
    collection_id = 11  # Replace with the actual collection_id you want to use
    specimen_data_entry = SpecimenDataEntryUI(collection_id)
    specimen_data_entry.show()
    specimen_data_entry.center_screen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

