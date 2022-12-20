# -*- coding: utf-8 -*-
"""
  Created on September 28, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Test collection module
"""
"""
PLEASE RUN THIS TEST USING -s :
 python -m pytest -s .\tests\test_collection.py
"""

from models import collection
import specify_interface
import global_settings
from getpass import getpass

sp = specify_interface.SpecifyInterface()
col = collection.Collection(29)
#The Botany collection ID is 29
global_settings.baseURL = "https://specify-snm.science.ku.dk/"
# The login function below will not work without the baseURL stated.
token = sp.login(username=input('enter username:'), passwd=getpass('enter password:'),
                 collectionid=29, csrftoken=sp.getCSRFToken())
baseUrl = "https://specify-snm.science.ku.dk/"

col.loadPredefinedData()

def test_prepTypes():
    prepTypes = [[i for i in j] for j in col.prepTypes]
    assert prepTypes[1][2] == 'sheet'

def test_typeStatus():
    typeStatus = [[i for i in j] for j in col.typeStatuses]
    assert typeStatus[0][2] == 'Allolectotype'

def test_storageLocation():
      storageLoc = [[i for i in j] for j in col.storageLocations]
      assert  storageLoc[1][2] == 'Box 2'

def test_georegions():
    georegions = [[i for i in j] for j in col.geoRegions]
    assert georegions[4][1] == 'America centralis et australis et Antarctica'

def test_getFields():
    fieldsDict = col.getFieldsAsDict()
    assert fieldsDict['spid'] == '688130'

def test_getSpecifyObject():
    # Testing the more generic version of getCollObject().
    # In this case collectionobject, but could be 'attachment', 'author' etc.
    res = sp.getSpecifyObject('collectionobject', 411590)
    assert res['catalognumber'] == '000864870'
