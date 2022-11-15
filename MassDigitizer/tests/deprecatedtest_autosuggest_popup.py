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
TESTDATAPATH = Path(__file__).parent

# Internal dependencies 
# none

# The module to be tested
import autoSuggest_popup as asp

# Instantiate taxonname autosuggest popup
aspTaxonNames = asp.AutoSuggest_popup('taxonname', 29)

# Instantiate storage autosuggest popup
aspStorage = asp.AutoSuggest_popup('storage', 29)

def test_taxonname():
    # Determine, rather trivially, whether the correct tablename has been set ('taxonname')
    assert aspTaxonNames.tableName == 'taxonname'

def test_taxonname_auto_suggest():

    choices = aspTaxonNames.captureSuggestion('pra', 'fullname')
    print(f'Got {len(choices)} taxon suggestions. ')
    found = False 
    for c in choices:
      #print(c['fullname'])
      if c['fullname'] == 'Poa pratensis': 
        found = True 
        break

    assert found

def test_storage_auto_suggest():
    # TODO 
    choices = aspStorage.captureSuggestion('Box', 'fullname')
    print(f'Got {len(choices)} storage suggestions. ')
    found = False 
    for c in choices:
      if c['fullname'] == 'Natural History Museum of Denmark | Priorparken | Herbarium C: Danish Vascular Plant Collection | Box 1': 
        found = True 
        break

    assert found