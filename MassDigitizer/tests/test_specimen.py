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

# Basal dependencies
import sys
import pytest

# The following lines allow for finding code files to be tested in the app root folder 
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.joinpath('MassDigitizer')))
TESTDATAPATH = Path(__file__).parent

import models.specimen as collobj

# Create blank specimen record instance 
specimenObject = collobj.Specimen(29)
predefData = None

def rowObjectToList(rowObject):
    toEnumeratedList = []
    for row in rowObject:
        itemList = [col for col in row]
        toEnumeratedList.append(itemList)
    # headers = ['id', 'spid', 'prep_type', 'collection_id']
    rowList = list(enumerate(toEnumeratedList))
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

    print('typestatus : ',  typeStatus[5][1][2])

    assert typeStatus[5][1][2] == 'Epitype'
    # NOTE A lowercase assertion ('hapantotype') would fail 

def test_prepType():
    specimenObject.loadPredefinedData()
    # for r in obj.prepTypes:
    #     print([j for j in r])
    assert specimenObject.prepTypes[1][2] == 'sheet'

def test_specimen_global():
    catalogNumber = set_specimen_global()
    assert (catalogNumber == 951754)

def test_georegions():
    geoList = []
    regions = specimenObject.geoRegions

    for j in regions:
        geoList.append([k for  k in j])
        # print('GEOREGIONS:::', [k for  k in j])
    enumGeo = list(enumerate(geoList))
    #print(enumGeo)
    # for item in enumGeo:
    #     print('GEOREGION:::', item )
    print('FINAL TEST : ', enumGeo[9][1][1])
    assert (enumGeo[9][1][1] == 'Island')

def test_storage():
    id = 3880
    storageList = []
    storageLoc = specimenObject.storageLocations
    for j in storageLoc:
        storageList.append([k for k in j])
    storager = list(enumerate(storageList))
    print('FINAL TEST : ', storager[3880][1][2])
    assert (storager[3880][1][2] == 'Shelf 8')

# def test_geosources():
#     sourceList = []
#     source = specimenObject.geoRegionSources
#     for j in source:
#         sourceList.append([k for k in j])
#     sourceMaster = list(enumerate(sourceList))
#     print('FINAL TEST : ', sourceMaster[1])
# Cannot test geoRegion-sources because source_collectionID is never 29 in table georegionsource ##

def test_getFieldsAsDictionary():
    fieldDict = specimenObject.getFieldsAsDict()
    lengthFieldDict= len(fieldDict)
    assert (lengthFieldDict == 25)

def test_memberOfFieldDict():
    res = specimenObject.getFieldsAsDict()
    dkeys = res.keys()
    assert ("storagefullname" in dkeys) == True

def test_load_previous():
    res = specimenObject.loadPrevious(30)
    
    if res is  None: 
        assert False
    else: 
        assert res

def test_save_load_delete():

    specimenSaved = False
    specimenLoaded = False 
    specimenIdLoaded = False
    specimenUpdated = False

    # 
    initialCatalogNumber = '12345678'
    specimenObject.catalogNumber = initialCatalogNumber
    specimenObject.save()
    savedSpecimenId = specimenObject.id
    if savedSpecimenId > 0: 
        specimenSaved = True
    else: assert False 

    # Test whether initial catalog number was saved and is re-loaded
    specimenObject.catalogNumber = ''
    specimenObject.load(savedSpecimenId)
    if specimenObject.catalogNumber == initialCatalogNumber:
        specimenLoaded = True
    else: assert False

    # Test whether Id is loaded 
    if specimenObject.id == savedSpecimenId & specimenObject.id > 0: 
        specimenIdLoaded = True
    else: assert False 

    # Test whether changes are updated 
    newCatalogNumber = '87654321'
    specimenObject.catalogNumber = newCatalogNumber
    specimenObject.save()
    specimenObject.catalogNumber = ''
    specimenObject.load(savedSpecimenId)
    if specimenObject.catalogNumber == newCatalogNumber:
        specimenUpdated = True
    else: assert False

    # Clean up record 
    specimenObject.delete()
    newSpecimenObject = collobj.Specimen(29)
    # 
    newSpecimenObject.load(savedSpecimenId)
    if newSpecimenObject.catalogNumber == '':
        specimenDeleted = True
    else: assert False

    assert specimenSaved and specimenLoaded and specimenIdLoaded and specimenUpdated and specimenDeleted





