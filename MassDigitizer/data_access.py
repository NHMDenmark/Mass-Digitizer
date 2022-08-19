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
from queue import Empty
import sys 
import sqlite3, json
from debugpy import connect

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.joinpath('src')))

# Point to database file 
FILEPATH = Path(__file__).parent.joinpath('db')
dbFilePath = str(FILEPATH.joinpath('db.sqlite3'))
currentCursor = Empty

def setDatabase(dbFileName='db'):
    # This optional function allows for setting a different database file like e.g. 'test' 
    # CONTRACT 
    #   dbFileName (String): the name of the file excluding the extension '.sqlite3' 
    dbFilePath = str(FILEPATH.joinpath('%s.sqlite3' % dbFileName))

# def setDbCursor(dbFilePath, in_memory=False):
#     # TODO
#     connection = sqlite3.connect('file:%s?mode=memory'%dbFilePath)
#     connection.row_factory = sqlite3.Row # Enable column access by name: row['column_name']
#
#     cursor = connection.cursor()

def getDbCursor():
    # Generic function needed for database access 
    #   RETURNS database cursor object 
    connection = sqlite3.connect(dbFilePath)
    connection.row_factory = sqlite3.Row # Enable column access by name: row['column_name']
    cursor = connection.cursor()
    return cursor

def getRows(tableName, limit=100):
    # Getting all rows from the table specified by name
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   limit (Integer) : The maximum number of rows - 0 means all rows 
    #   RETURNS table rows (list)
    print('Get all rows from table "%s" ...' % tableName)
    cursor = getDbCursor()
    sqlString = "SELECT * FROM " + tableName
    if limit > 0:
        sqlString += ' LIMIT %s' %str(limit)
    rows = cursor.execute(sqlString).fetchall()
    print('found %d rows ' % len(rows))
    cursor.connection.close()
    return rows

def getRowsOnFilters(tableName, filters, limit=100):
    # Getting specific rows specified by filters from the table specified by name
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   filters (Dictionary) :  A dictionary where the key is the field name and the value is the field filter *including operand*!
    #                           The operand should be included with the field and any string values should be enclosed in "" 
    #                           Example: {'rankid': '=180', 'taxonname': '="Felis"', 'taxonid' : 'IS NOT NULL'}  
    #   limit (Integer) : The maximum number of rows - 0 means all rows 
    #       NOTE: Strings should be formatted with enclosing double quotation marks (") 
    #             Numbers should be formatted as strings 
    #   RETURNS table rows (list)
    cursor = getDbCursor()
    sqlString = 'SELECT * FROM %s ' % tableName 
    if filters.items():
        sqlString += "WHERE "
        for key, value in filters.items():
            sqlString += '%s %s AND ' % (key, str(value))
    sqlString = sqlString[0:len(sqlString)-4] # Remove trailing " AND "
    if limit > 0:
        sqlString += ' LIMIT %s' %str(limit)
    #print(sqlString)
    rows = cursor.execute(sqlString).fetchall()
    cursor.connection.close()
    return rows

def getRowOnId(tableName, id):
    # Getting specific row from the table specified by name using its primary key (id)  
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   id (Integer) : The primary key of the row to be returned 
    #   RETURNS single table row 
    cursor = getDbCursor()
    row = cursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
    cursor.connection.close()
    return row

def getRowOnSpecifyId(tableName, id):
    # Getting specific row from the table specified by name using the primary key of the corresponding table in Specify
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   id (Integer) : The primary key of the row to be returned 
    #   RETURNS single table row 
    cursor = getDbCursor()
    row = cursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
    cursor.connection.close()
    return row

def insertRow(tableName, fields):
    # Inserting a row of field values into a table specified by name
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   fields (Dictionary) : A dictionary where the key is the field name and the value is the field value 
    #       NOTE: Strings should be formatted with enclosing double quotation marks (") 
    #             Numbers should be formatted as strings 
    #   RETURNS SQL result (String)
    cursor = getDbCursor()
    fieldsString = ""
    for key in fields:
        fieldsString += "%s, " % key
    fieldsString  = fieldsString[0:len(fieldsString)-2]
    sqlString = "INSERT INTO %s (%s) VALUES (" %(tableName, fieldsString)
    for key in fields:
        sqlString += str(fields[key]) + ", "
    sqlString = sqlString[0:len(sqlString)-2] + ");" # Remove trailing ", " and close Sql 
    #print(sqlString)
    cursor.execute(sqlString)
    cursor.connection.commit()
    cursor.connection.close()
    return "Row [%s] inserted in table '%s'" %(fields,tableName)

def getFieldMap(cursor):
    # Get fields for a given DB API 2.0 cursor object that has been executed
    # CONTRACT 
    #   cursor (Cursor) : Cursor object to be field mapped 
    #   RETURNS a dictionary that maps each field name to a column index; 0 and up.
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1
    return results

setDatabase()