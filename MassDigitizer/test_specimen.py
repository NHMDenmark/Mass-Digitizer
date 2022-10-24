# -*- coding: utf-8 -*-
"""
  Created on October 14, 2022
  @author: Jan K. Legind, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  PURPOSE: Unit testing the specimen class.
"""


import pytest
import sys
import models

import numpy as np

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.joinpath('MassDigitizer')))


TESTDATAPATH = Path(__file__).parent

import models.specimen as collobj

specimenObject = collobj.specimen(29)
predefData = None

def rowObjectToList(rowObject):
    toEnumeratedList = []
    for row in rowObject:
        itemList = [col for col in row]
        toEnumeratedList.append(itemList)
    # headers = ['id', 'spid', 'prep_type', 'collection_id']
    rowList = list(enumerate(toEnumeratedList))
    print('orig rowLList ', list(rowList))
    return rowList

def set_specimen_global():
    errors = []
    specimenObject.catalogNumber = 951754
    global predefData
    predefData = specimenObject.loadPredefinedData()
    return specimenObject.catalogNumber


def test_specimen_prepTypes():
    global predefData
    print(predefData)
    sObject = specimenObject.typeStatuses
    typeStatus = rowObjectToList(sObject)
    # print('--', typeStatus, '--')
    print('typestatus : ',  typeStatus[5][1][2])
    assert typeStatus[5][1][2] == 'Hapantotype'
    # Knowing for a fact that typeStatus[5][1][2] is 'Hapantotype',
    #I expect a lowercase assertion to fail: 'hapantotype'

def test_predefined():
    specimenObject.loadPredefinedData()
    # for r in obj.prepTypes:
    #     print([j for j in r])
    assert specimenObject.prepTypes[0][2] == 'sheet'

def test_specimen_global():
    catalogNumber = set_specimen_global()
    assert (catalogNumber == 951754)

def test_georegions():
    geoList = []
    regions = specimenObject.geoRegions
    list(enumerate(regions))
    for j in regions:
        geoList.append([k for  k in j])
        # print('GEOREGIONS:::', [k for  k in j])
    enumGeo = list(enumerate(geoList))
    print(enumGeo)
    for item in enumGeo:
        print('GEOREGION:::', item )
    print('FINAL TEST : ', enumGeo[9][1][1])
    assert (enumGeo[9][1][1] == 'Island')

def test_storage():
    id = 3880




