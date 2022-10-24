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

  PURPOSE: Unit testing the specify_interface module.
"""
import specify_interface
import global_settings as gs
import pytest

baseUrl = "https://specify-snm.science.ku.dk/"

gs.baseURL = baseUrl

def test_getCSRFToken():
    token = specify_interface.getCSRFToken()
    print('the token X:DDDDDDDD\n', token)
    print(len(token))
    assert token

def test_lengthCSRF_token():
    token = specify_interface.getCSRFToken()
    assert len(token) == 64