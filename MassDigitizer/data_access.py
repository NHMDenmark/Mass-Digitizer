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

class DataAccess(): 

    def __init__(self,databaseName='db', do_in_memory=False):
        """
        Initialize for database access 
            CONTRACT
               do_in_memory (boolean): Whether the database file should be run in-memory 
        NOTE Database file is installed into user documents folder otherwise it would be readonly on a Windows PC in any case 
        """

        self.currentCursor = None   # Reset cursor pointer 
        
        # Point to database file provided and connect
        filePath = os.path.expanduser('~\Documents\DaSSCO') # In order to debug / run, a copy of the db file should be moved into this folder on Windows machines 
        altFilePath = os.path.expanduser('~\OneDrive - University of Copenhagen\Documents\DaSSCO') # For OneDrive users this is the file location 
        self.dbFilePath = str(Path(filePath).joinpath(f'{databaseName}.sqlite3'))
        self.dbAltFilePath = str(Path(altFilePath).joinpath(f'{databaseName}.sqlite3'))
        #self.setDatabase(databaseName)
        #print('Initializing with db file: %s ...'%self.dbFilePath)
        self.connection = sqlite3.connect(self.dbFilePath)
        
        if gs.db_in_memory == True or do_in_memory == True:
            #print(' - running database in-memory')
            # Read database to tempfile
            tempfile = StringIO()
            for line in self.connection.iterdump():
                tempfile.write('%s\n' % line)
            self.connection.close()
            tempfile.seek(0)

            # Create a database in memory and import from tempfile
            self.connection = sqlite3.connect(":memory:")
            self.connection.cursor().executescript(tempfile.read())
            self.connection.commit()
        else:
            #print(' - running database as file')
            pass

        self.connection.row_factory = sqlite3.Row
        self.currentCursor = self.connection.cursor()

    def setDatabase(self, dbFileName='db'):
        # This optional function allows for setting a different database file like e.g. 'test' 
        # CONTRACT 
        #   dbFileName (String): the name of the file excluding the extension '.sqlite3' 
        self.dbFilePath = str(Path(self.dbFilePath).joinpath(f'{dbFileName}.sqlite3'))
        self.dbAltFilePath = str(Path(self.dbAltFilePath).joinpath(f'{dbFileName}.sqlite3'))
        print(self.dbFilePath)

    def getConnection(self):
        self.connection = sqlite3.connect(self.dbFilePath)
        return self.connection

    def getDbCursor(self):#do_in_memory=False):
        # Generic function needed for database access 
        # CONTRACT
        #   TODO: do_in_memory (boolean): Whether the database file should be run in-memory 
        #   RETURNS database cursor object 
        #print(f'Connecting to db file: {self.dbFilePath} ...')

        # Connect to database file. On error, try alternative location assuming OneDrive user
        try:
            self.connection = sqlite3.connect(self.dbFilePath)    # Normal user 
        except:
            self.connection = sqlite3.connect(self.dbAltFilePath) # Assumed OneDrive user
        
        # Depending on in-memory flag, run database in memory 
        # TODO Momentarily deactivated, perhaps redundant 
        #gs.db_in_memory = do_in_memory # apply in-memory flag to global  
        if gs.db_in_memory == True:
            #print(' - running database in-memory')
            # Read database to tempfile
            tempfile = StringIO()
            for line in self.connection.iterdump():
                tempfile.write('%s\n' % line)
            self.connection.close()
            tempfile.seek(0)

            # Create a database in memory and import from tempfile
            self.connection = sqlite3.connect(":memory:")
            self.connection.cursor().executescript(tempfile.read())
            self.connection.commit()
        else:
            #print(' - running database as file')
            pass

        self.connection.row_factory = sqlite3.Row # Enable column access by name: row['column_name']
        cursor = self.connection.cursor()
        #print('Connection established')
        return cursor

    def getRows(self, tableName, limit=100, sortColumn=None):
        # Getting all records from the table specified by name
        # CONTRACT 
        #   tableName (String): The name of the table to be queried
        #   limit (Integer) : The maximum number of records - 0 means all records 
        #   sortColumn (String) : The column to sort the rows on, if any 
        #   RETURNS table rows (list)
        currentCursor = self.getDbCursor()        
        #print('Get all rows from table "{%s}" ...' % tableName)

        sqlString = f'SELECT * FROM {tableName}' 
        
        if limit > 0:
            sqlString += f' LIMIT {limit}'
        
        if sortColumn is not None: 
            sqlString += f' ORDER BY {sortColumn}'
        print(sqlString)
        records = currentCursor.execute(sqlString).fetchall()
        
        #print(f'Found {len(records)} records ')
        
        self.currentCursor.connection.close()
        
        return records

    def getRowsOnFilters(self, tableName, filters, limit=10000, sort=None):
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
        currentCursor = self.getDbCursor()   
        #print(f'-> getRowsONFilter({tableName}, {filters}, {limit})')
        sqlString = 'SELECT * FROM %s ' % tableName

        if filters.items():
            sqlString += "WHERE "
            for key, value in filters.items():
                sqlString += f'{key} {value} AND '
        sqlString = sqlString[0:len(sqlString)-4] # Remove trailing " AND "
        
        if sort is not None: 
            sqlString += f' ORDER BY {sort}'
        
        if limit > 0:
            sqlString += f' LIMIT {limit}'

        print(sqlString)
        
        records = currentCursor.execute(sqlString).fetchall()
        
        currentCursor.connection.close()

        return records

    def getRowOnId(self, tableName, id):
        # Getting specific row from the table specified by its primary key (id)  
        # CONTRACT 
        #   tableName (String): The name of the table to be queried
        #   id (Integer) : The primary key of the row to be returned
        #   RETURNS single table row
        currentCursor = self.getDbCursor()   
        record = currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
        currentCursor.connection.close()

        return record

    def getRowOnSpId(self, tableName, spid):
        # Getting specific row from the table specified by its Specify primary key (spid)  
        # CONTRACT 
        #   tableName (String): The name of the table to be queried
        #   spid (Integer) : The Specify primary key of the row to be returned
        #   RETURNS single table row
        currentCursor = self.getDbCursor()   
        record = currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(spid)).fetchone()
        currentCursor.connection.close()

        return record

    def deleteRowOnId(self, tableName, id):
        """
        Deleting specific row from the table specified by its primary key (id)  
        CONTRACT 
        tableName (String): The name of the table to be queried
        id (Integer) : The primary key of the row to be returned
        """
        currentCursor = self.getDbCursor()
        print(f'DELETE FROM {tableName} WHERE id = {id};')   
        currentCursor.execute(f'DELETE FROM {tableName} WHERE id = {id};')
        currentCursor.connection.commit()
        currentCursor.connection.close()

    def getMaxRow(self, tableName):
        # Get the row from the specified table with the highest primary key (id) 
        # CONTRACT 
        #   tableName (String): The name of the table to be queried
        #   RETURNS single table row (SQLITErow)
        currentCursor = self.getDbCursor()
        sql = f'SELECT MAX({tableName}.id) FROM {tableName};'
        record = currentCursor.execute(sql).fetchone()
        currentCursor.connection.close()
        #print(f'record: {record}')
        return record

    def executeSqlStatement(self, sql):
        # Execute specified sql statement 
        # CONTRACT 
        #   sql (String) : 
        #   RETURNS table rows as dictionary
        self.currentCursor = self.getDbCursor()
        
        # records = [dict(row) for row in rows_object]
        # print('in data-access: The row(s) = ', records)
        # for j in records:
        #     print(j)
            # print([x for x in j])

        rows = self.currentCursor.execute(sql).fetchall()

        self.currentCursor.connection.commit()
        self.currentCursor.connection.close()

        return rows

    def getRowOnSpecifyId(self, tableName, id):
        # Getting specific row from the table specified by name using the primary key of the corresponding table in Specify
        # CONTRACT 
        #   tableName (String): The name of the table to be queried
        #   id (Integer) : The primary key of the row to be returned 
        #   RETURNS single table row 
        self.currentCursor = self.getDbCursor()   
        record = self.currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
        self.currentCursor.connection.close()
        
        return record

    def insertRow(self, tableName, fields):
        # Inserting a row of field values into a table specified by name
        # CONTRACT 
        #   tableName (String): The name of the table to be queried
        #   fields (Dictionary) : A dictionary where the key is the field name and the value is the field value 
        #       NOTE: Strings should be formatted with enclosing double quotation marks (") 
        #             Numbers should be formatted as strings 
        #   RETURNS inserted record row
        self.currentCursor = self.getDbCursor()   
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
        
        valuesSql = '","'.join(sqlValues)
        valuesSql = f'"{valuesSql}")'
        sqlString = sqlString + valuesSql
        self.currentCursor.execute(sqlString)
        self.currentCursor.connection.commit()
        recordID = self.currentCursor.lastrowid
        record = self.currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(recordID)).fetchone()
        self.currentCursor.connection.close()

        return record

    def updateRow(self, tableName, recordID, values, where='', sqlString=None):
        # TODO Function contract 
        #   RETURNS updated record row
        self.currentCursor = self.getDbCursor()
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
                    #print(val)
                    val = '"'+val+'"'
                    #print('new val:', val)
                    sqlString = f"{key} = {val}, "
                    sqlStringAppend.append(sqlString)

                except AttributeError:
                    #print('ATTRIBUTE ERRRORRRRRR')
                    sqlStringAppend.append(values[key])
            sqlStringLastPart = " WHERE id = {}".format(recordID)
            try:

                sqlAdd = ' '.join(sqlStringAppend)

                sqlAdd = sqlAdd[:-2]

                sqlStringFinal = sqlStringPrepend+' '+sqlAdd+sqlStringLastPart
                #print('FINAL SQL is : ', sqlStringFinal)
            except TypeError:
                #print('IN sql build except typeError!')
                sqlStringFinal = ','.join(map(str, sqlStringAppend))

            #print('SQL going into execute: ', sqlStringFinal)

        self.currentCursor.execute(sqlStringFinal)
        self.currentCursor.connection.commit()
        record = self.currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(recordID)).fetchone()
        self.currentCursor.connection.close()

        return record 

    def getFieldMap(self):
        # Get fields for a given DB API 2.0 cursor object that has been executed
        # CONTRACT 
        #   cursor (Cursor) : Cursor object to be field mapped 
        #   RETURNS a dictionary that maps each field name to a column index; 0 and up.
        currentCursor = self.getDbCursor()   
        results = {}
        column = 0
        for d in currentCursor.description:
            results[d[0]] = column
            column = column + 1
        
        return results

db = DataAccess('test')
