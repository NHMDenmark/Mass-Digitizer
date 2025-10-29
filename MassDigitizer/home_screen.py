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
import socket, requests
from urllib3.exceptions import MaxRetryError

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtCore import QTimer

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
        QTimer.singleShot(0, self.auto_login) # Attempt auto-login if login.cfg exists

    def load_ui(self):
        loader = QUiLoader()
        ui_path = util.resourcePath("ui/homescreen.ui")
        util.logger.debug(f'Loading UI from {ui_path}')
        ui_file = QFile(ui_path)
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

    def auto_login(self):
        """ 
        Auto-login using credentials from login.cfg file if it exists 
        """

        config_path = Path(util.getUserPath()).joinpath('config').joinpath('login.cfg')
        print(f'Checking for auto-login config at {config_path}')
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    lines = f.readlines()
                    credentials = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in lines if ':' in line}
                
                username = credentials.get('username', '')
                password = credentials.get('password', '')
                institution_name = credentials.get('institution', '')
                collection_name = credentials.get('collection', '')

                # Set username and password
                if username: self.ui.inpUsername.setText(username)
                if password: self.ui.inpPassword.setText(password)

                if institution_name and collection_name:
                    # Set institution
                    index = self.ui.lstSelectInstitution.findText(institution_name)
                    if index != -1:
                        self.ui.lstSelectInstitution.setCurrentIndex(index)
                        self.on_institution_selected()  # Manually trigger to load collections

                        # Set collection
                        index = self.ui.lstSelectCollection.findText(collection_name)
                        if index != -1:
                            self.ui.lstSelectCollection.setCurrentIndex(index)
                            collection = self.select_collection(collection_name)

                            # Attempt login
                            self.login(username, password, collection)
                        else:
                            util.logger.warning(f'Collection "{collection_name}" not found for institution "{institution_name}".')
                    else:
                        util.logger.warning(f'Institution "{institution_name}" not found.')
                else:
                    util.logger.warning('Incomplete credentials in login.cfg.')
            except Exception as e:
                util.logger.error(f'Error during auto-login: {e}')
        else:
            util.logger.info('No login.cfg file found for auto-login.')

    def on_institution_selected(self):        
        self.selected_institution = self.ui.lstSelectInstitution.currentText()
        if self.selected_institution == "-please select-":
            self.ui.lstSelectCollection.clear()
            self.ui.btnLogin.setEnabled(False)  # Disable login button
            return
        
        try:
            util.logger.debug(f'Selected institution: {self.selected_institution}')
            institution = db.getRowsOnFilters('institution', {' name = ':f'"{self.selected_institution}"'}, 1)
            self.institution_id = institution[0]['id']
            self.institution_url = institution[0]['url']
            gs.baseURL = self.institution_url
            collections = util.convert_dbrow_list(db.getRowsOnFilters('collection', {' institutionid = ':f'{self.institution_id}', 'visible = ': '1'}), True)
            self.ui.lstSelectCollection.clear()
            self.ui.lstSelectCollection.addItems(collections)
            pass
        except Exception as e:
            util.logger.error(f'Error selecting institution: {e}')
            self.ui.lstSelectCollection.clear()

    def on_collection_selected(self):
        collection_name = self.ui.lstSelectCollection.currentText()
        if collection_name and collection_name != "-please select-":
            self.ui.btnLogin.setEnabled(True)  # Enable login button
            self.select_collection(collection_name)
        else:
            self.ui.btnLogin.setEnabled(False)  # Disable login button
        
    def select_collection(self, collection_name=None):
        if collection_name:
            collection_lookup = db.getRowsOnFilters('collection', {'name = ':f'"{collection_name}"' , 'institutionid = ':f'{self.institution_id}',})
            if collection_lookup and collection_lookup[0]['id'] > 0:
                self.selected_collection = coll.Collection(collection_lookup[0]['id'])
                self.ui.lstSelectCollection.setCurrentText(collection_name)
        
        if self.selected_collection: 
            util.logger.debug(f'Selected collection: {self.selected_collection.name}')
        return self.selected_collection

    def on_login_clicked(self):
        username = self.ui.inpUsername.text()
        password = self.ui.inpPassword.text()
        
        selected_collection = self.select_collection(self.ui.lstSelectCollection.currentText())

        if not username or not password:
            self.ui.lblIncomplete.setVisible(True)
            return
        
        self.login(username, password, selected_collection)
        
    def login(self, username, password, collection):

        if collection and collection.id > 0:
            collection_id = collection.id
            gs.baseURL = self.institution_url
            try:
                gs.csrfToken = sp.specifyLogin(username, password, collection.spid)
            except (requests.exceptions.RequestException, MaxRetryError, socket.gaierror, OSError) as e:
                # Network / connection related errors
                util.logger.error("Login failed: Unable to connect to Specify server.", exc_info=True)
                self.show_error_message(f"Unable to connect to Specify server. Please check your network connection or try opening the site in a browser: \n {self.institution_url} ")
                self.ui.lblConnectionError.setVisible(True)
                return
            except Exception as e:
                # Fallback for any other unexpected exceptions
                util.logger.error(f"An unexpected error occurred during login: {e}\n{traceback.format_exc()}")
                self.show_error_message(str(e))
                return

            if gs.csrfToken != '': # TODO Check token format for extra security 
                # Login was successful

                gs.userName = username
                gs.collection = collection 
                gs.collectionName = collection.name
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
                
                try:
                    util.logger.info("Login successful, launching SpecimenDataEntryUI")
                    self.specimen_ui = sde.SpecimenDataEntryUI(collection_id)
                    self.specimen_ui.show()
                    self.hide()
                except Exception as e:
                    util.logger.error(f"Failed to load SpecimenDataEntryUI: {e}")
                    self.show()
                    self.show_error_message(e)
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