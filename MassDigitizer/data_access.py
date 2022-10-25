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

import os
#import sys 
import sqlite3
from io import StringIO
from pathlib import Path

# Local imports
import global_settings as gs

# Set os path to local files: 
#sys.path.append(str(Path(__file__).parent.parent.joinpath('MassDigitizer')))

#class DataAccess: 
# TODO turn into class 

# Moved database file to user documents (Windows) otherwise it will be readonly 
dbFilePath = os.path.expanduser('~\Documents\DaSSCO\db.sqlite3') # In order to debug / run, a copy of the db file should be moved into this folder on Windows machines 
dbAltFilePath = os.path.expanduser('~\OneDrive - University of Copenhagen\Documents\DaSSCO\db.sqlite3') # For OneDrive users this is the file location 

# Reset cursor pointer 
currentCursor = None
connection = None

# Point to database file 
def __init__(self,databaseName='db', do_in_memory=False):
    # Initialize for database access 
    # CONTRACT
    #   do_in_memory (boolean): Whether the database file should be run in-memory 

    self.set_database(databaseName)
    print('Initializing with db file: %s ...'%self.dbFilePath)
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

def getDbCursor():#do_in_memory=False):
    # Generic function needed for database access 
    # CONTRACT
    #   TODO: do_in_memory (boolean): Whether the database file should be run in-memory 
    #   RETURNS database cursor object 
    print('Connecting to db file: %s ...'%dbFilePath)

    # Connect to database file. On error, try alternative location assuming OneDrive user
    try:
        connection = sqlite3.connect(dbFilePath)    # Normal user 
    except:
        connection = sqlite3.connect(dbAltFilePath) # Assumed OneDrive user
    
    # Depending on in-memory flag, run database in memory 
    # TODO Momentarily deactivated, perhaps redundant 
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

    connection.row_factory = sqlite3.Row # Enable column access by name: row['column_name']
    cursor = connection.cursor()
    print('Connection established')
    return cursor

def getRows(tableName, limit=100, sortColumn=None):
    # Getting all records from the table specified by name
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   limit (Integer) : The maximum number of records - 0 means all records 
    #   sortColumn (String) : The column to sort the rows on, if any 
    #   RETURNS table rows (list)
    currentCursor = getDbCursor()        
    print('Get all rows from table "{%s}" ...' % tableName)

    sqlString = f'SELECT * FROM {tableName}' 
    
    if limit > 0:
        sqlString += f' LIMIT {limit}'
    
    if sortColumn is not None: 
        sqlString += f' ORDER BY {sortColumn}'

    records = currentCursor.execute(sqlString).fetchall()
    
    print(f'Found {len(records)} records ')
    
    currentCursor.connection.close()
    
    return records

def getRowsOnFilters(tableName, filters, limit=10000):
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
    print(f'-> getRowsONFilter({tableName}, {filters}, {limit})')
    sqlString = 'SELECT * FROM %s ' % tableName
    print('    - ', sqlString)
    if filters.items():
        sqlString += "WHERE "
        for key, value in filters.items():
            sqlString += f'{key} {value} AND '
    sqlString = sqlString[0:len(sqlString)-4] # Remove trailing " AND "
    if limit > 0:
        sqlString += f' LIMIT {limit}'
    print(sqlString)
    try:
        records = currentCursor.execute(sqlString).fetchall()
    # If no records in results, insert an empty dummy row to prevent errors
        if len(records) < 1:
            records = currentCursor.execute("SELECT * FROM dummyrecord LIMIT 1").fetchall()
            currentCursor.connection.close()
    except sqlite3.OperationalError:
        records = currentCursor.execute("SELECT * FROM dummyrecord LIMIT 1").fetchall()
        currentCursor.connection.close()

    return records

def getRowOnId(tableName, id):
    # Getting specific row from the table specified by name using its primary key (id)  
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   id (Integer) : The primary key of the row to be returned
    #   RETURNS single table row
    currentCursor = getDbCursor()   
    record = currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
    currentCursor.connection.close()

    return record

def getMaxRow(tableName):
    # Get the row from the specified table with the highest primary key (id) 
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   RETURNS single table row (SQLITErow)
    currentCursor = getDbCursor()
    sql = f'SELECT MAX({tableName}.id) FROM {tableName};'
    record = currentCursor.execute(sql).fetchone()
    currentCursor.connection.close()
    print(f'record: {record}')
    return record

def executeSqlStatement(sql):
    # Execute specified sql statement 
    # CONTRACT 
    #   sql (String) : 
    #   RETURNS table rows as dictionary
    currentCursor = getDbCursor()
    
    # records = [dict(row) for row in rows_object]
    # print('in data-access: The row(s) = ', records)
    # for j in records:
    #     print(j)
        # print([x for x in j])

    rows = currentCursor.execute(sql).fetchall()

    currentCursor.connection.commit()
    currentCursor.connection.close()

    return rows


def getRowOnSpecifyId(tableName, id):
    # Getting specific row from the table specified by name using the primary key of the corresponding table in Specify
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   id (Integer) : The primary key of the row to be returned 
    #   RETURNS single table row 
    currentCursor = getDbCursor()   
    record = currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
    currentCursor.connection.close()
    
    return record

def insertRow(tableName, fields):
    # Inserting a row of field values into a table specified by name
    # CONTRACT 
    #   tableName (String): The name of the table to be queried
    #   fields (Dictionary) : A dictionary where the key is the field name and the value is the field value 
    #       NOTE: Strings should be formatted with enclosing double quotation marks (") 
    #             Numbers should be formatted as strings 
    #   RETURNS inserted record row
    currentCursor = getDbCursor()   
    fieldsString = ""
    for key in fields:
        fieldsString += "%s, " % key
    fieldsString  = fieldsString[0:len(fieldsString)-2]
    sqlString = f"INSERT INTO {tableName} ({fieldsString}) VALUES ("
    sqlValues = []
    for key in fields:
        addSql = fields[key].replace('""', '')
        sqlValues.append(addSql)
        sqlValues = [item.replace('"', '') for item in sqlValues]
    
    finSql = '","'.join(sqlValues)
    finSql = '"'+finSql+'")'
    finSql = sqlString+finSql
    print(' -> ', finSql)

    # sqlString += str(formattedSql) + ','
    # sqlList = ['"' + item + '",' for item in sqlValues]
    # formattedSql = ''.join(sqlList)
    # print('The sqlVALS are: ', ''.join(sqlList))
    # sqlString = sqlString+formattedSql
    # sqlString = sqlString[0:len(sqlString)-1] + ");" # Remove trailing ", " and close Sql
    # print('final sql', sqlString)

    currentCursor.execute(finSql)
    currentCursor.connection.commit()
    recordID = currentCursor.lastrowid
    record = currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(recordID)).fetchone()
    currentCursor.connection.close()

    return record

def updateRow(tableName, recordID, values, where='', sqlString=None):
    # TODO Function contract 
    #   RETURNS updated record row
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
                val = val.replace('"', '')
                print(val)
                val = '"'+val+'"'
                print('new val:', val)
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
    record = currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(recordID)).fetchone()
    currentCursor.connection.close()

    return record 


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

