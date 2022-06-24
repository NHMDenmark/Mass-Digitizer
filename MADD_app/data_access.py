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

  PURPOSE: Generic Data Access Object for reading/writing local database file 
  """
import sqlite3, json

def getRows(tableName):
    # Getting all rows from the table specified by name
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   RETURNS table rows (list)
    print('Get all rows from table "%s" ...' % tableName)
    connection = sqlite3.connect('db\db.sqlite3')
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM " + tableName).fetchall()
    print('found %d rows ' % len(rows))
    connection.close()
    return rows

def getRowOnId(tableName, id):
    # Getting specific row from the table specified by name using its primary key (id)  
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   id (Integer) : The primary key of the row to be returned 
    #   RETURNS single table row 
    connection = sqlite3.connect('db\db.sqlite3')
    cursor = connection.cursor()
    row = cursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
    connection.close()
    return row

def getRowOnSpecifyId(tableName, id):
    # Getting specific row from the table specified by name using the primary key of the corresponding table in Specify
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   id (Integer) : The primary key of the row to be returned 
    #   RETURNS single table row 
    connection = sqlite3.connect('db\db.sqlite3')
    cursor = connection.cursor()
    row = cursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
    connection.close()
    return row

def getRowsOnFilters(tableName, filters):
    # Getting specific rows specified by filters from the table specified by name
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   filters (Dictionary) : A dictionary where the key is the field name and the value is the field filter 
    #       NOTE: Strings should be formatted with enclosing double quotation marks (") 
    #             Numbers should be formatted as strings 
    #   RETURNS table rows (list)
    connection = sqlite3.connect('db\db.sqlite3')
    cursor = connection.cursor()
    sqlString = 'SELECT * FROM %s ' % tableName 
    if filters.items():
        sqlString += "WHERE "
    for key, value in filters.items():
        sqlString += '%s = %s AND ' % (key, str(value))
    sqlString = sqlString[0:len(sqlString)-4] # Remove trailing " AND "
    print(sqlString)
    rows = cursor.execute(sqlString).fetchall()
    connection.close()
    return rows

def insertRow(tableName, fields):
    # TODO 
    connection = sqlite3.connect('db\db.sqlite3')
    cursor = connection.cursor()
    sqlString = "INSERT INTO %s "
    for key in fields:
        print('key')
    pass

    connection.close()

def getFieldMap(cursor):
    """ Given a DB API 2.0 cursor object that has been executed, returns
    a dictionary that maps each field name to a column index; 0 and up. """
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1
    return results



# CODE STUB JUNKYARD 

"""
institutions = json.load(open('bootstrap/institutions.json'))
for institution in institutions:
    pass
"""

# print(getRowsOnFilters('institutions', {'code': '"TEST"','id' : '0'}))

"""
print('---')
print(getRows('institutions'))
print('---')
print(getRowOnId('institutions', 0))
print('---')
print(getRowsOnFilters('institutions', [{'code': 'TEST'}]))
"""