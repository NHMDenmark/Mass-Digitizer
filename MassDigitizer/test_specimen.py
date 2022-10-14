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

def rowEater(rowObject):
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
    typeStatus = rowEater(sObject)
    # print('--', typeStatus, '--')
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