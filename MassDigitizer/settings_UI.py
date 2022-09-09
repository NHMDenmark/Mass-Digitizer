# -*- coding: utf-8 -*-
"""
  Created on September 9, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: User interface for managing application-wide settings. 
"""

import PySimpleGUI as sg

# Internal 
import data_access as db
import util

collections = db.getRows('collection')
collList = util.convert_dbrow_list(collections)

layout = [[sg.Text('collections'), sg.Combo(collList, enable_events=True, key='cbxCollections', size=(30, 1))],]
window = sg.Window('testing', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event =='cbxCollections':
        text = values[event]
        index = window[event].widget.current()
        id = collections[index]['id'] 
        spid = collections[index]['spid'] 
        print(index, id, spid, repr(values[event]))

window.close()