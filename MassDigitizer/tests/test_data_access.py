# -*- coding: utf-8 -*-
"""
  Created on October 14, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Unit testing the data access layer 
"""

# Basal dependencies
import sys 
import pytest

# The following lines allow for finding code files to be tested in the app root folder  
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.joinpath('MassDigitizer')))

#Internal dependencies 
import util 
import models

# The module to be tested
import data_access as db

def test_data_access_getRows():
    # Generic test of fetching records from the local database 
    # Institutions is a stable table with expected values 

    institutions = util.convert_dbrow_list(db.getRows('institution'))

    # If no records fetched throw error 
    assert len(institutions) > 0 




