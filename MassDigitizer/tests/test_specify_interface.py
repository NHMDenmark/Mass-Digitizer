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

from queue import Empty

baseUrl = "https://specify-snm.science.ku.dk/"

gs.baseURL = baseUrl
tokenGL = ''
CSRF = ''

def test_getCSRFToken():
    token = spLogin()
    global tokenGL
    tokenGL = token
    print('the token X:DDDDDDDD\n', token)
    print(len(token))
    assert token

def test_login():
    tkCSFR = spLogin()
    print('In test_login() --- tok:', tkCSFR)
    global CSRF
    CSRF = tkCSFR
    print('CRF::', CSRF)
    assert tkCSFR

def test_getCSRFToken():
    token = specify_interface.getCSRFToken()
    global tokenGL
    tokenGL = token
    assert token


def test_lengthCSRF_token():
    token = specify_interface.getCSRFToken()
    # Be aware that CSRF tokens can be of different lengths, depending on implementation.
    assert len(token) == 64


def test_login():
    #
    pass


def test_getCollObject():
    if tokenGL: print("TOKENNNNN =====", CSRF)
    res = specify_interface.getCollObject(29, CSRF)

    assert res


def test_getSpecifyObject():
    token = spLogin()
    res = specify_interface.getSpecifyObject('collectionobject', 411590, token)

    if res is not Empty:
        print(res['catalognumber'])
    else:
        print('empty')
    assert res


def test_getInitialCollection():
    res = specify_interface.getInitialCollections()

    assert res[688130] == "NHMD Vascular Plants"

def test_verify_Session():
    valid = specify_interface.verifySession(tokenGL)

    assert valid

def spLogin():
    # Securing against accidental github commits of credentials.
    return specify_interface.login(username=input('enter username:'), passwd=getpass('enter password:'),
                                   collectionid=29, csrftoken=specify_interface.getCSRFToken())
