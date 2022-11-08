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

  PURPOSE: Unit testing the util module
"""
import util
import data_access
import global_settings as gs

db = data_access.DataAccess(gs.databaseName)

rows = db.getRows('taxonname', 1000)
# Global rows fetchall() object for test use.

def test_shrink_dict():
    fnameDict = {}

    # Loop populates dict with fullname as keys.
    for j in rows:
        fnameDict[j[3]] = ''

    #print(len(fnameDict))
    resShrink = util.shrink_dict(fnameDict, 'Pot')
    assert len(resShrink) == 19

def test_convert_dbrow_list():
    res = util.convert_dbrow_list(rows)
    #print(res)
    assert res