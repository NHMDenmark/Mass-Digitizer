# -*- coding: utf-8 -*-
"""
  Created on 2022-06-21
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  Plants of the World Online taxonomy https://hosted-datasets.gbif.org/datasets/wcvp.zip is used in this exploration.

  PURPOSE: Generic Data Access Object for reading/writing local database file 
  """
import sqlite3, json

def getRows(tableName):
    connection = sqlite3.connect('db\db.sqlite3')
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM " + tableName).fetchall()
    connection.close()
    return rows

def getRowOnId(tableName, id):
    connection = sqlite3.connect('db\db.sqlite3')
    cursor = connection.cursor()
    row = cursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
    connection.close()
    return row

def getRowsOnFilters(tableName, filters):
    connection = sqlite3.connect('db\db.sqlite3')
    cursor = connection.cursor()
    sqlString = "SELECT * FROM " + tableName + " "
    if filters.items():
        sqlString += "WHERE "
    for key, value in filters.items():
        sqlString += "" + key + " = "  + value + " AND "
    sqlString = sqlString[0:len(sqlString)-4] # Remove trailing " AND "
    print(sqlString)
    rows = cursor.execute(sqlString).fetchall()
    connection.close()
    return rows

institutions = json.load(open('bootstrap/institutions.json'))
for institution in institutions:
    pass

print(getRowsOnFilters('institutions', {'code': '"TEST"','id' : '0'}))

"""
print('---')
print(getRows('institutions'))
print('---')
print(getRowOnId('institutions', 0))
print('---')
print(getRowsOnFilters('institutions', [{'code': 'TEST'}]))
"""