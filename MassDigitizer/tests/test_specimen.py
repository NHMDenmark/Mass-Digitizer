import pytest
import sys
import models

import numpy as np

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.joinpath('MassDigitizer')))


TESTDATAPATH = Path(__file__).parent

import specimen as collobj

specimenObject = collobj.specimen(29)

def test_specimen():
    specimenObject.catalogNumber = 951754
    preDefData = specimenObject.loadPredefinedData()
    x=0
    y=3
    assert x == y
    assert specimenObject.catalogNumber == 951753

def test_specimen2():
    record = specimenObject.getFieldsAsDict()
    assert specimenObject.geoRegionId == 24

def test_predefined():
    specimenObject.loadPredefinedData()
    # for r in obj.prepTypes:
    #     print([j for j in r])
    assert specimenObject.prepTypes[0][2] == 'sheet'



