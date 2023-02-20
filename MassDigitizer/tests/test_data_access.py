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

import sys 
import pytest

# Internal dependencies 
import global_settings as gs

# The following lines allow for finding code files to be tested in the app root folder  
""" from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.joinpath('MassDigitizer')))
TESTDATAPATH = Path(__file__).parent """

#Internal dependencies 
import util 
import models

# The module to be tested
import data_access

db = data_access.DataAccess('test')

def test_getRows():
    # Generic test of fetching records from the local database 
    # Institutions is a stable table with expected values 

    institutions = db.getRows('institution')

    # If no records fetched throw error 
    assert len(institutions) > 0 

def test_getRowsOnFilters():
    # Generic test of fetching records from the local db on a filter 

    # Institution code is unique so should yield a single record 
    institutions = db.getRowsOnFilters('institution', {'code' : '="NHMD"'})

    # If single record fetched then test has passed
    assert len(institutions) == 1 

def test_getRowsOnFilters_Multiple():
    # Generic test of fetching multiple records from the local db on a filter 

    # A specific number of institutions have "Museum" in their name   
    institutions = db.getRowsOnFilters('institution', {'name' : 'LIKE "%Museum%"'})

    # Exactly 5 records fetched 
    assert len(institutions) == 5
    
"""    # Check each record to be correct one
    assert institutions[0]['code'] == 'NHMD'
    assert institutions[1]['code'] == 'NHMA'
    assert institutions[2]['code'] == 'MMG'
    assert institutions[3]['code'] == 'MSJN'
    assert institutions[4]['code'] == 'OESM' """

def test_getRowsOnFilters_Multiple_Max():
    # Generic test of fetching multiple records from the local db on a filter and a max entries 

    # Five institutions have "Museum" in their name, but we only want the first 2 fetched
    institutions = db.getRowsOnFilters('institution', {'name' : 'LIKE "%Museum%"'}, 2)

    # Exactly 2 records fetched 
    assert len(institutions) == 2

def test_getRowOnId():
    # Generic test of fetching specific records from the local db on primary key
     
    # The institution with pk=1 should be NHMD 
    institution = db.getRowOnId('institution', 1)

    # NHMD record fetched 
    assert institution['code'] == 'NHMD'

def test_getMaxRow():
    # TODO Generic test of fetching specific records from the local db on primary key

    institutions = db.getRows('institution', 0, 'id')

    # Get last institution in list, which also has the highest id 
    lastInstitution = institutions[len(institutions)-1]
    
    # Run function to be tested 
    maxIdInstitution = db.getMaxRow('institution') # THIS fucker

    # Check whether both record IDs match
    assert lastInstitution['id'] == maxIdInstitution['id']

def test_executeSqlStatement():

    pass



