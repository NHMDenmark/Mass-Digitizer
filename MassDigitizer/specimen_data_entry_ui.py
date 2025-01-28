# -*- coding: utf-8 -*-

"""
Created on Fri Jan 24 2025 11:12:00 
Author: Fedor Alexander Steeman NHMD;

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

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QLineEdit, QComboBox, QRadioButton, QCheckBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QStandardPaths
from PySide6.QtGui import QFont, QIcon, QPixmap
from pathlib import Path

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
        self.db = data_access.DataAccess(gs.databaseName)  # Instantiate database access module
        self.collobj = specimen.Specimen(collection_id)  # Create blank specimen record instance

        # Load UI and setup connections
        self.load_ui()
        self.setup_connections()
        self.setup(collection_id)

        self.collectionId = collection_id  # Set collection Id
        self.collection = coll.Collection(collection_id)
        self.window = None  # Create class level instance of window object
        self.db = data_access.DataAccess(gs.databaseName)  # Instantiate database access module
        self.collobj = specimen.Specimen(collection_id)  # Create blank specimen record instance

        # Create recordset of last 3 saved records for the initial preview table
        self.recordSet = recordset.RecordSet(collection_id, 3,specimen_id=self.collobj.id) 

         # Load data
        self.load_comboboxes()
        self.load_previous_records()

        # Set image resource
        documents_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        image_path = os.path.join(documents_path, "DaSSCo", "img", "Warning_LinkedRecord.png")
        self.ui.imgWarningLinkedRecord.setPixmap(QPixmap(image_path))

        # Start up interface
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

        # Specify the columns to display by their headers
        columns_to_display = ['id', 'catalognumber', 'taxonfullname', 'containertype', 'georegionname', 'storagename']

        # Iterate over the records in the recordSet
        for record in self.recordSet.records:
            row_position = self.ui.tblPrevious.rowCount()
            self.ui.tblPrevious.insertRow(row_position)

            # Add only the specified columns to the table
            for column_index, column_header in enumerate(columns_to_display):
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
        ui_file = QFile("ui/specimendataentry.ui")
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

    def setup_connections(self):
        """
        Setup connections between signals and slots.
        """

        # Connect signals to slots
        for line_edit in self.findChildren(QLineEdit):
            line_edit.returnPressed.connect(self.focusNextChild)

        for combo_box in self.findChildren(QComboBox):
            combo_box.currentIndexChanged.connect(self.focusNextChild)
        
        for radio_button in self.findChildren(QRadioButton):
            radio_button.toggled.connect(self.on_containerTypeToggle)

        # Explicitly set focus for checkboxes
        self.ui.chkDamage.clicked.connect(lambda: self.ui.chkSpecimenObscured.setFocus())
        self.ui.chkSpecimenObscured.clicked.connect(lambda: self.ui.chkLabelObscured.setFocus())
        self.ui.chkLabelObscured.clicked.connect(lambda: self.ui.radRadioSSO.setFocus())

        # Explicitly set focus for radio buttons
        #self.ui.radRadioSSO.toggled.connect(lambda: self.ui.inpNotes.setFocus())
        #self.ui.radRadioMOS.toggled.connect(lambda: self.ui.inpContainerName.setFocus())
        #self.ui.radRadioMSO.toggled.connect(lambda: self.ui.inpContainerName.setFocus())
        
        self.ui.btnSave.clicked.connect(self.on_save_clicked)
        self.ui.btnBack.clicked.connect(self.on_back_clicked)
        self.ui.btnForward.clicked.connect(self.on_forward_clicked)
        self.ui.btnClear.clicked.connect(self.on_clear_clicked)

    def setup(self, collection_id):
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
        """
        self.ui.inpNotes.returnPressed.connect(self.on_notes_return_pressed)
        self.ui.inpContainerName.returnPressed.connect(self.on_container_name_return_pressed)

    def on_containerTypeToggle(self, checked):
        """
        Set container type controls events.
        """
        sender = self.sender()
        print(sender)
        
        if checked:
            if sender == self.ui.radRadioSSO:
                # A single specimen object does not require a container name
                self.ui.inpContainerName.setText('')
                self.ui.inpContainerName.setEnabled(False)
                self.ui.imgWarningLinkedRecord.setVisible(False)
            elif sender == self.ui.radRadioMOS or sender == self.ui.radRadioMSO:
                # A multi specimen object requires a container name and a warning to the user
                containerNumber = util.getRandomNumberString()
                containerType = ''
                if sender == self.ui.radRadioMOS:
                    containerType = 'MOS'
                elif sender == self.ui.radRadioMSO:
                    containerType = 'MSO'
                newContainerName = containerType + str(containerNumber)
                self.ui.inpContainerName.setText(newContainerName)
                self.ui.inpContainerName.setEnabled(True)
                self.ui.imgWarningLinkedRecord.setVisible(True)

            self.ui.inpNotes.setFocus()

    def on_save_clicked(self):
        print("Save button clicked")

    def on_back_clicked(self):
        print("Back button clicked")

    def on_forward_clicked(self):
        print("Forward button clicked")

    def on_clear_clicked(self):
        print("Clear button clicked")

    def on_notes_return_pressed(self):
        print("Notes return pressed")

    def on_container_name_return_pressed(self):
        print("Container name return pressed")

    def updateRecordCount(self):
        print("Update record count")

    def center_screen(self):
        # Get the existing QApplication instance
        app = QApplication.instance()

        # Center the window on the screen
        screen = app.primaryScreen()
        center = screen.availableGeometry().center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

def main():
    app = QApplication(sys.argv)
    collection_id = 11  # Replace with the actual collection_id you want to use
    specimen_data_entry = SpecimenDataEntryUI(collection_id)
    specimen_data_entry.show()
    specimen_data_entry.center_screen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()