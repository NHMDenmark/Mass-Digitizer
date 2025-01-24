# -*- coding: utf-8 -*-

"""
Created on Fri Jan 24 2025 11:12:00 
@authors: Fedor Alexander Steeman NHMD;

Copyright 2022 Natural History Museum of Denmark (NHMD)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import sys
import time 
import traceback

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QFont, QIcon, QScreen
from pathlib import Path

# Internal dependencies
import util
import data_access
import global_settings as gs
import autoSuggest_popup
from models import specimen
from models import model
from models import recordset
from models import collection as coll
import specify_interface

class SpecimenDataEntry(QMainWindow):
    def __init__(self, collection_id):
        super(SpecimenDataEntry, self).__init__()

        # Set class variables
        self.collection_id = collection_id
        self.collection = coll.Collection(collection_id)
        self.db = data_access.DataAccess(gs.databaseName)  # Instantiate database access module
        self.collobj = specimen.Specimen(collection_id)  # Create blank specimen record instance

        # Load UI and setup connections
        self.load_ui()
        self.setup_connections()
        self.setup(collection_id)

    def load_ui(self):
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
        self.ui.btnSave.clicked.connect(self.on_save_clicked)
        self.ui.btnBack.clicked.connect(self.on_back_clicked)
        self.ui.btnForward.clicked.connect(self.on_forward_clicked)
        self.ui.btnClear.clicked.connect(self.on_clear_clicked)

    def setup(self, collection_id):
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
        self.ui.inpNotes.returnPressed.connect(self.on_notes_return_pressed)
        self.ui.inpContainerName.returnPressed.connect(self.on_container_name_return_pressed)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    specimen_data_entry = SpecimenDataEntry(collection_id=11)
    
    specimen_data_entry.show()

    # Center the window on the screen
    screen = app.primaryScreen()
    center = screen.availableGeometry().center()
    geo = specimen_data_entry.frameGeometry()
    geo.moveCenter(center)
    specimen_data_entry.move(geo.topLeft())
    
    sys.exit(app.exec_())