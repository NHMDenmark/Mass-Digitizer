# -*- coding: utf-8 -*-
"""
  Created on August 16, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: The home screen or starting point of the application, where the user is asked to choose institution and log in.  
"""

from pathlib import Path
import traceback

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

# Internal dependencies
import util
import global_settings as gs
import models.collection as coll
import data_access
import specify_interface
import specimen_data_entry_ui as sde

db = data_access.DataAccess(gs.databaseName)
sp = specify_interface.SpecifyInterface()

class HomeScreen(QMainWindow):
    # Get version number to set into the homeScreen welcome menu.
    version = util.getVersionNumber()    
    util.logger.debug(f'Starting Mass Digitizer App version {version}')

    def __init__(self):
        super(HomeScreen, self).__init__()
        self.load_ui()
        self.setup_connections()

    def load_ui(self):
        loader = QUiLoader()
        ui_file = QFile("ui/homescreen.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set window properties
        imgPath = str(Path(util.getUserPath()).joinpath(f'img/DaSCCo-logo.png'))
        self.setWindowIcon(QIcon(imgPath))  # Update the path to icon file
        self.setWindowTitle("DaSSCo Mass Digitizer")

        # Set version number
        current_version = util.getVersionNumber()
        self.ui.header.setText(f"DaSSCo Mass Digitizer App - Version {current_version}")

        # Preload the contents of lstSelectInstitution
        self.institutions = util.convert_dbrow_list(db.getRowsOnFilters('institution', {'visible = ': 1})) or ["-please select-"]
        self.ui.lstSelectInstitution.addItem("-please select-")
        self.ui.lstSelectInstitution.addItems(self.institutions)
        self.ui.lstSelectInstitution.setCurrentIndex(0)

    def setup_connections(self):
        self.ui.lstSelectInstitution.currentIndexChanged.connect(self.on_institution_selected)
        self.ui.lstSelectCollection.currentIndexChanged.connect(self.on_collection_selected)
        self.ui.btnLogin.clicked.connect(self.on_login_clicked)  # Connect login button
        self.ui.btnExit.clicked.connect(self.close)

    def on_institution_selected(self):
        try:
            self.selected_institution = self.ui.lstSelectInstitution.currentText()
            if self.selected_institution == "-please select-":
                self.ui.lstSelectCollection.clear()
                self.ui.btnLogin.setEnabled(False)  # Disable login button
                return

            util.logger.debug(f'Selected institution: {self.selected_institution}')
            institution = db.getRowsOnFilters('institution', {' name = ':f'"{self.selected_institution}"'}, 1)
            self.institution_id = institution[0]['id']
            self.institution_url = institution[0]['url']
            gs.baseURL = self.institution_url
            collections = util.convert_dbrow_list(db.getRowsOnFilters('collection', {' institutionid = ':f'{self.institution_id}', 'visible = ': '1'}), True)
            self.ui.lstSelectCollection.clear()
            self.ui.lstSelectCollection.addItems(collections)
        except Exception as e:
            util.logger.error(f'Error selecting institution: {e}')
            self.ui.lstSelectCollection.clear()

    def on_collection_selected(self):
        selected_collection = self.ui.lstSelectCollection.currentText()
        if selected_collection and selected_collection != "-please select-":
            self.ui.btnLogin.setEnabled(True)  # Enable login button
        else:
            self.ui.btnLogin.setEnabled(False)  # Disable login button

    def on_login_clicked(self):
        username = self.ui.inpUsername.text()
        password = self.ui.inpPassword.text()
        
        if not username or not password:
            self.ui.lblIncomplete.setVisible(True)
            return

        selected_collection = self.ui.lstSelectCollection.currentText()
        collection = db.getRowsOnFilters('collection', {'name = ':f'"{selected_collection}"' , 'institutionid = ':f'{self.institution_id}',})
        
        if collection and collection[0]['id'] > 0:
            collection_id = collection[0]['id']
            gs.baseURL = self.institution_url
            gs.csrfToken = sp.specifyLogin(username, password, collection[0]['spid'])

            if gs.csrfToken != '': # TODO Check token format for extra security 
                # Login was successful

                gs.userName = username
                gs.collectionName = selected_collection
                gs.collection = coll.Collection(collection_id)
                gs.institutionId = self.institution_id
                gs.institutionName = self.selected_institution 

                # 1. Fetch SpecifyUser on username (/api/specify/specifyuser/?name=username)
                users = sp.getSpecifyObjects('specifyuser', filters={"name": username})
                if not users:
                    self.show_error_message("User not found in Specify database.")
                    return
                user = users[0]
                gs.spUserId = user['id']

                # 2. Fetch Agent on specifyuser primary key (/api/specify/agent/?specifyuser=n)
                agents = sp.getSpecifyObjects('agent', filters={"specifyuser": gs.spUserId})
                if not agents:
                    self.show_error_message("Agent details not found for the user.")
                    return
                agent = agents[0]

                # 3. Store full name in global settings (as single, concatenated string of first, middle, last)
                gs.firstName = agent['firstname']
                gs.middleInitial = agent['middleinitial']
                gs.lastName = agent['lastname']

                self.hide()
                
                try:
                    util.logger.info("Login successful, launching SpecimenDataEntryUI")
                    self.specimen_ui = sde.SpecimenDataEntryUI(collection_id)
                    self.specimen_ui.show()
                except Exception as e:
                    util.logger.error(f"Failed to load SpecimenDataEntryUI: {e}")
                    self.show()
                    self.show_error_message(e)

                else:
                    self.ui.lblAuthError.setVisible(True)
            else:
                self.ui.lblAuthError.setVisible(True)
        else:
            self.ui.lblCollError.setVisible(True)
        
    def show_error_message(self, message):
            # Log full traceback
            util.logger.error(f"An unexpected error occurred: {message}\n{traceback.format_exc()}")

            # Show error popup
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("An unexpected error occurred while loading the Specimen Data Entry UI.")
            error_dialog.setInformativeText(str(message))  # Show the error message
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec()

if __name__ == "__main__":
    app = QApplication([])
    home_screen = HomeScreen()
    home_screen.show()
    app.exec()