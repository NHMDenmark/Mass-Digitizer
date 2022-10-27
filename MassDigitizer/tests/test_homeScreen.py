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

  PURPOSE: Unit testing the home_screen module
"""

import home_screen
import util
import data_access as db

import pytest

def test_institutions():
    #In def init() there is an important institutions list var.
    # hs = home_screen.init()
    institutionList = util.convert_dbrow_list(db.getRows('institution'))
    print('""""""""', institutionList)
    assert len(institutionList) > 1

"""
Login CSRF token validation is tested in test_specify_interface and specify_interface.py
is included in the home_screen module. 
"""