#-*- coding: utf-8 -*-
"""
Created on Thu May 26 17:44:00 2022

@author: Jan K. Legind, NHMD

Copyright 2022 Natural History Museum of Denmark (NHMD)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""
import data_access
from itertools import chain

def small_list_lookup(tableName, inputKey, indicesForColumn=2):
    ###For retreiving values stored in the minor tables ('institution' and 'collection')
    #tableName: String can be 'Storage location', ' Prep type' , 'institution', etc.
    #inputKey: Is the field key from the specimen_data_entry interface like: Prep type, Broad geographic region

    #return: content of particular table

    rows = data_access.getRows(tableName, limit=200)

    result = rows
    return result


def auto_suggest_taxonomy(name, taxDefItemId=None, rowLimit=2000):
    # Purpose: for helping digitizer staff rapidly input names by returning suggestions based on the three or
    #  more entered characters.
    #trigger: means how many keystrokes it takes to trigger the auto-suggest functionality
    #rowLimit: at or below this the auto-suggest fires of its names
    #returns: a list of names

    cur = data_access.getDbCursor()
    sql = "SELECT fullname FROM taxonname WHERE lower(fullname) LIKE lower('{}%');".format(name)
    if taxDefItemId:
        sql = sql[:-1]
        sql = sql + ' AND taxontreedefid = {};'.format(taxDefItemId)
        print(sql)
    rows = cur.execute(sql).fetchall()

    print('len rows = ', len(rows))
    lengthOfRows =len(rows)
    if lengthOfRows <= rowLimit:
        print('AUTOSUGGEST!!!')
        flatCandidates = list(chain.from_iterable(rows))
        # print(flatCandidates)
        rows = list(flatCandidates)

        return rows , lengthOfRows

###TEST AREA
# outcome = auto_suggest_taxonomy('Rosa rug', taxDefItemId=13)
# # outcome = small_list_lookup('institution', 'k')
# if outcome:
#     print('outcome sörenme,,, ',type(outcome[0]), outcome)
#     for elem in outcome:
#     # print(elem['name'])
#         print('length of outcome = ', outcome[1])
#
# else:
#     print('NO outcome')