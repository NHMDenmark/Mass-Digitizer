# -*- coding: utf-8 -*-
"""
  Created on October 14, 2022
  @author: Jan K. Legind, NHMD
  @author: Fedor Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Unit testing the specify_interface module.
"""

import specify_interface
import global_settings as gs
from pprint import pprint
from getpass import getpass

class Test_specify_interface():
    """ 
        
    """

    def __init__(self) -> None:

        gs.baseURL = "https://specify-test.science.ku.dk/"

        self.collectionID = 29
        
        self.sp = specify_interface.SpecifyInterface()    
        self.token = self.sp.getCSRFToken()        

    def test_getCSRFToken(self):
        assert self.token

    def test_spLogin(self):

        userName = input('enter username:')
        passWord = getpass('enter password:')

        self.token = self.sp.login(userName, passWord, self.collectionID, self.token)

    def test_lengthCSRF_token(self):
        token = self.sp.getCSRFToken()
        # NOTE Be aware that CSRF tokens can be of different lengths, depending on implementation.
        assert len(token) == 64

    def test_getCollObject(self):
        # Tests obtaining a collection object (JSON) from the specify API.
        # Foreknowledge of a collectionID is required (in this case 411590).
        res = self.sp.getCollObject(411590, self.token)
        assert res

    def test_getSpecifyObject(self):
        # Testing the more generic version of getCollObject().
        # In this case collectionobject, but could be 'attachment', 'author' etc.
        res = self.sp.getSpecifyObject('collectionobject', 411590, self.token)
        assert res

    def test_getInitialCollection(self):
        res = self.sp.getInitialCollections()
        assert res[688130] == "NHMD Vascular Plants"

    def test_verify_Session(self):
        valid = self.sp.verifySession(self.token)
        assert valid

    def test_getDiscipline(self):
        disciplineId = 688129
        disciplineObj = self.sp.getSpecifyObject('discipline', disciplineId, self.token)

        assert disciplineObj