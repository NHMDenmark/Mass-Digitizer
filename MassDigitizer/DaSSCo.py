# -*- coding: utf-8 -*-
"""
  Created on September 22, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: The execution starting point of the application.
"""

import sys
import traceback 
from PySide6.QtWidgets import QApplication, QMessageBox

# Internal dependencies
import util
import global_settings as gs
import data_access
import specify_interface
import specimen_data_entry as sde
from home_screen import HomeScreen

db = data_access.DataAccess(gs.databaseName)
sp = specify_interface.SpecifyInterface()

def main():
    try:
        app = QApplication(sys.argv)
        home_screen = HomeScreen()
        home_screen.show()
        sys.exit(app.exec())
    except Exception as e:
        traceBack = traceback.format_exc()
        util.logger.error(f'{e} \n\n {traceBack}')
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setText(f'{e} \n\n {traceBack}')
        error_msg.setWindowTitle('Error')
        error_msg.exec()

if __name__ == "__main__":
    main()