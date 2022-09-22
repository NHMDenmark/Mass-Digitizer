# -*- coding: utf-8 -*-
"""
  Created on 2022-09-22
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Exporting data from local database 
"""

from pandas import DataFrame as pdf

# local imports
import data_access as db

specimens = db.getRowsOnFilters('specimen', {'exported':'IS NULL'},100000)

print('Found %s specimens: '%len(specimens))

for specimen in specimens:
    print(' - ', specimen['taxonname'])