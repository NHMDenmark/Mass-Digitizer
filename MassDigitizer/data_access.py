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

import sys 
import sqlite3
from io import StringIO
from pathlib import Path

# Local imports
import global_settings as gs

# Set os path to local files: 
#sys.path.append(str(Path(__file__).parent.parent.joinpath('MassDigitizer')))

#class DataAccess:
#FILEPATH =  #Path(__file__).parent.joinpath('db')
dbFilePath = Path(__file__).resolve().with_name('db.sqlite3') #str(FILEPATH.joinpath('db.sqlite3'))
currentCursor = None

# Point to database file 
def __init__(self,databaseName='db', do_in_memory=False):
    # Initialize for database access 
    # CONTRACT
    #   do_in_memory (boolean): Whether the database file should be run in-memory 

    self.set_database(databaseName)
    print('Connecting to db file: %s ...'%self.dbFilePath)
    connection = sqlite3.connect(self.dbFilePath)
    
    if gs.db_in_memory == True or do_in_memory == True:
        print(' - running database in-memory')
        # Read database to tempfile
        tempfile = StringIO()
        for line in connection.iterdump():
            tempfile.write('%s\n' % line)
        connection.close()
        tempfile.seek(0)

        # Create a database in memory and import from tempfile
        connection = sqlite3.connect(":memory:")
        connection.cursor().executescript(tempfile.read())
        connection.commit()
    else:
        #print(' - running database as file')
        pass

    connection.row_factory = sqlite3.Row
    currentCursor = connection.cursor()


def setDatabase(self, dbFileName='db'):
    # This optional function allows for setting a different database file like e.g. 'test' 
    # CONTRACT 
    #   dbFileName (String): the name of the file excluding the extension '.sqlite3' 
    dbFilePath = str(self.FILEPATH.joinpath('%s.sqlite3' % dbFileName))

def getConnection():
    connection = sqlite3.connect(dbFilePath)
    return connection


connection = None
def getDbCursor():#do_in_memory=False):
    # Generic function needed for database access 
    # CONTRACT
    #   do_in_memory (boolean): Whether the database file should be run in-memory 
    #   RETURNS database cursor object 
#     connection = sqlite3.connect(dbFilePath)
#     connection.row_factory = sqlite3.Row # Enable column access by name: row['column_name']
#     cursor = connection.cursor()
#     return cursor

# def get_inmemory_cursor(in_memory=True):
#     # TODO write function contract
    print('Connecting to db file: %s ...'%dbFilePath)
    connection = sqlite3.connect(dbFilePath)
    
    #gs.db_in_memory = do_in_memory # apply in-memory flag to global  
    if gs.db_in_memory == True:
        print(' - running database in-memory')
        # Read database to tempfile
        tempfile = StringIO()
        for line in connection.iterdump():
            tempfile.write('%s\n' % line)
        connection.close()
        tempfile.seek(0)

        # Create a database in memory and import from tempfile
        connection = sqlite3.connect(":memory:")
        connection.cursor().executescript(tempfile.read())
        connection.commit()
    else:
        #print(' - running database as file')
        pass

    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    return cursor


def getRows(tableName, limit=100):
    # Getting all rows from the table specified by name
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   limit (Integer) : The maximum number of rows - 0 means all rows 
    #   RETURNS table rows (list)
    currentCursor = getDbCursor()        
    print('Get all rows from table "%s" ...' % tableName)
    sqlString = "SELECT * FROM " + tableName
    if limit > 0:
        sqlString += ' LIMIT %s' %str(limit)
    rows = currentCursor.execute(sqlString).fetchall()
    print('found %d rows ' % len(rows))
    currentCursor.connection.close()
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
    #   RETURNS table rows as list
    currentCursor = getDbCursor()   
    sqlString = 'SELECT * FROM %s ' % tableName
    print('IN getRowsONFilter - the SQL is: ', sqlString, '//STOP//')
    if filters.items():
        sqlString += "WHERE "
        for key, value in filters.items():
            sqlString += '%s %s AND ' % (key, str(value))
    sqlString = sqlString[0:len(sqlString)-4] # Remove trailing " AND "
    if limit > 0:
        sqlString += ' LIMIT %s' %str(limit)
    print(sqlString)
    try:
        rows = currentCursor.execute(sqlString).fetchall()
    # If no rows in results, insert an empty dummy row to prevent errors
        if len(rows) < 1:
            rows = currentCursor.execute("SELECT * FROM dummyrecord LIMIT 1").fetchall()
            currentCursor.connection.close()
    except sqlite3.OperationalError:
        rows = currentCursor.execute("SELECT * FROM dummyrecord LIMIT 1").fetchall()
        currentCursor.connection.close()
    return rows

def getRowOnId(tableName, id, maxID=False):
    # Getting specific row from the table specified by name using its primary key (id)  
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   id (Integer) : The primary key of the row to be returned
    #maxID is added functionality to get the latest record ID
    #   RETURNS single table row
    if maxID:
        currentCursor = getDbCursor()
        sql = "SELECT MAX({}.id) FROM {};".format(tableName, tableName)
        row = currentCursor.execute(sql).fetchone()
        currentCursor.connection.close()
        return row

    currentCursor = getDbCursor()   
    row = currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
    currentCursor.connection.close()
    return row

def executeSqlStatement(sql):
    currentCursor = getDbCursor()
    rows_object = currentCursor.execute(sql).fetchall()
    rows = [dict(row) for row in rows_object]
    # print('in data-access: The row(s) = ', rows)
    for j in rows:
        print(j)
        # print([x for x in j])
    currentCursor.connection.close()
    return rows


def getRowOnSpecifyId(tableName, id):
    # Getting specific row from the table specified by name using the primary key of the corresponding table in Specify
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   id (Integer) : The primary key of the row to be returned 
    #   RETURNS single table row 
    currentCursor = getDbCursor()   
    row = currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
    currentCursor.connection.close()
    return row

def insertRow(tableName, fields):
    # Inserting a row of field values into a table specified by name
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   fields (Dictionary) : A dictionary where the key is the field name and the value is the field value 
    #       NOTE: Strings should be formatted with enclosing double quotation marks (") 
    #             Numbers should be formatted as strings 
    #   RETURNS SQL result (String)
    currentCursor = getDbCursor()   
    fieldsString = ""
    for key in fields:
        fieldsString += "%s, " % key
    fieldsString  = fieldsString[0:len(fieldsString)-2]
    sqlString = "INSERT INTO %s (%s) VALUES (" %(tableName, fieldsString)
    for key in fields:
        sqlString += str(fields[key]) + ", "
    sqlString = sqlString[0:len(sqlString)-2] + ");" # Remove trailing ", " and close Sql 
    print(sqlString)
    currentCursor.execute(sqlString)
    currentCursor.connection.commit()
    currentCursor.connection.close()
    return "Row [%s] inserted in table '%s'" %(fields,tableName)


def updateRow(tableName, recordID, values, where='', sqlString=None):
    # Funtion is patterned after insertRow()
    currentCursor = getDbCursor()
    fieldsString = ""

    for key in values:
        fieldsString += "%s, " % key

    if len(where) > 1:
        print('adding ', where, ' to sql')
    else:
        # Building the SQL query string below
        sqlStringPrepend = f"UPDATE {tableName} SET "
        sqlStringAppend = []

        for key in values:
            try:
                val = values[key]

                sqlString = f"{key} = {val}, "
                sqlStringAppend.append(sqlString)

            except AttributeError:
                print('ATTRIBUTE ERRRORRRRRR')
                sqlStringAppend.append(values[key])
        sqlStringLastPart = " WHERE id = {}".format(recordID)
        try:

            sqlAdd = ' '.join(sqlStringAppend)

            sqlAdd = sqlAdd[:-2]

            sqlStringFinal = sqlStringPrepend+' '+sqlAdd+sqlStringLastPart
            print('FINAL SQL is : ', sqlStringFinal)
        except TypeError:
            print('IN sql build except typeError!')
            sqlStringFinal = ','.join(map(str, sqlStringAppend))

        print('SQL going into execute: ', sqlStringFinal)
    currentCursor.execute(sqlStringFinal)
    currentCursor.connection.commit()
    currentCursor.connection.close()
    return "Row [%s] inserted in table '%s'" % (values, tableName)


def getFieldMap(cursor):
    # Get fields for a given DB API 2.0 cursor object that has been executed
    # CONTRACT 
    #   cursor (Cursor) : Cursor object to be field mapped 
    #   RETURNS a dictionary that maps each field name to a column index; 0 and up.
    currentCursor = getDbCursor()   
    results = {}
    column = 0
    for d in currentCursor.description:
        results[d[0]] = column
        column = column + 1
    return results

#init()