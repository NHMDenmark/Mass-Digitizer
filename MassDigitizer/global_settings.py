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

  PURPOSE: Assemblage of global settings used across the application.

  PURPOSE of sharedValidation: Make available a globally shared JSON struct to hold variables like 'catalog number length' :
  {"catalogNumberLength_NHMDvascularPlants": 8, "catalogNumberLength_NHMDentomology": 9} which can be used in multiple places.
"""

from shared import Dossier, HOME
from pathlib import Path

import os
# Shared JSON struct

validationData ={"catalogNumberLength_NHMDvascularPlants": 8, "catalogNumberLength_NHMDentomology": 9, "catalogNumberLength_NHMAentomology": 8}
path = Path(HOME, 'shared_vars')
validationGlobal = Dossier(path)
validationGlobal.set('shared_vars', validationData)

shared_out = validationGlobal.get("shared_vars")
print('shared_out', shared_out)

# Specify 
baseURL = ''

# database 
databaseName = 'db'
db_in_memory = False

# session 
institutionId = 0
institutionName = ''
collectionId = 0
collectionName = ''
firstName = ''
middleInitial = ''
lastName = ''
userName = ''
spUserId = -1
# agentFullName = ' '.join([spFirstName, spMiddleInitial, spLastName])
csrfToken = ''
lengthCatalogNumber = 0

def clearSession():
  institutionId = 0
  institutionName = '-not set-'
  collectionId = 0
  collectionName = '-not set-'
  spUserName = '-not set-'
  spUserId = -1
  csrfToken = ''
