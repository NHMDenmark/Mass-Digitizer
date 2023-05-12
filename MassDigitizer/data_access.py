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

import sqlite3
from pathlib import Path

# Local imports
import util

class DataAccess():

    def __init__(self, databaseName='db', do_in_memory=False):
        """
        Initialize for database access
            CONTRACT
               do_in_memory (boolean): Whether the database file should be run in-memory
        NOTE Database file is installed into user documents folder otherwise it would be readonly on a Windows PC in any case
        """
        #util.logger.debug("Initializing Data Access module...")
        try:
            self.currentCursor = None  # Reset cursor pointer
            # Point to database file provided and connect
            self.filePath = util.getUserPath()

            self.dbFilePath = str(Path(self.filePath).joinpath(f'{databaseName}.sqlite3'))
        except Exception as e:
            util.logger.debug(e)

        #util.logger.debug(('Connecting to database file: %s ...' % self.dbFilePath))

        try:
            self.connection = sqlite3.connect(self.dbFilePath)
        except Exception as e:

            util.logger.debug("SQLite connection failed. Error: %s" % e)
            logError = f"The path {self.dbFilePath} may not exist."
            util.logger.debug(logError)
            
        self.connection.row_factory = sqlite3.Row

        try:
            self.currentCursor = self.connection.cursor()
        except Exception as e:
            util.logger.debug(e)

    def setDatabase(self, dbFileName='db'):
        """
        This optional function allows for setting a different database file like e.g. 'test'
          CONTRACT
            dbFileName (String): the name of the file excluding the extension '.sqlite3'
        """
        self.dbFilePath = str(Path(util.getUserPath()).joinpath(f'{dbFileName}.sqlite3'))
        #util.logger.info("Database filepath: %s" % self.dbFilePath)

    def getConnection(self):
        """
        Returns the database connection initiated, if any
        """
        self.connection = sqlite3.connect(self.dbFilePath)
        return self.connection

    def getDbCursor(self):  # do_in_memory=False):
        """
        Generic function needed for database access
        CONTRACT
          RETURNS database cursor object
        """
        #util.logger.info(f'Connecting to db file: {self.dbFilePath} ...')
        self.connection = sqlite3.connect(self.dbFilePath)  # Normal user
        self.connection.row_factory = sqlite3.Row  # Enable column access by name: row['column_name']
        cursor = self.connection.cursor()
        #util.logger.info('Connection established')
        return cursor

    def getRows(self, tableName, limit=100, sortColumn=None):
        """
        Getting all records from the table specified by name
        CONTRACT
          tableName (String): The name of the table to be queried
          limit (Integer) : The maximum number of records - 0 means all records
          sortColumn (String) : The column to sort the rows on, if any
          RETURNS table rows (list)
        """
        currentCursor = self.getDbCursor()

        sqlString = f'SELECT * FROM {tableName}'

        if sortColumn is not None:
            sqlString += f' ORDER BY {sortColumn}'            

        if limit > 0:
            sqlString += f' LIMIT {limit}'
        
        #util.logger.info(sqlString)

        try:
            records = currentCursor.execute(sqlString).fetchall()
        except Exception as e:
            util.logger.debug(sqlString)
            util.logger.error(e)
            records = None
            
        self.currentCursor.connection.close()

        return records

    def getRowsOnFilters(self, tableName, filters, limit=10000, sort=None, descending=False):
        """
        Getting specific rows specified by filters from the table specified by name
        CONTRACT
          tableName (String): The name of the table to be queried
          filters (Dictionary) :  A dictionary where the key is the field name and the value is the field filter *including operand*!
                                  The operand should be included with the field and any string values should be enclosed in ""
                                  Example: {'rankid': '=180', 'taxonname': '="Felis"', 'taxonid' : 'IS NOT NULL'}
          limit (Integer) : The maximum number of rows - 0 means all rows
              NOTE: Strings should be formatted with enclosing double quotation marks (")
                    Numbers should be formatted as strings
          RETURNS table rows as list
        """
        self.currentCursor = self.getDbCursor()

        sqlString = 'SELECT * FROM %s ' % tableName

        if filters.items():
            sqlString += "WHERE "
            for key, value in filters.items():
                sqlString += f'{key} {value} AND '
        sqlString = sqlString[0:len(sqlString) - 4]  # Remove trailing " AND "

        # Add sorting if set 
        if sort: sqlString += f' ORDER BY {sort}'
        # Add sorting direction if descending 
        if descending: sqlString += ' DESC'
        # Add range (row limit) if set 
        if limit > 0: sqlString += f' LIMIT {limit}'
        util.logger.debug(sqlString)

        try:
            records = self.currentCursor.execute(sqlString).fetchall()
        except Exception as e:
            util.logger.debug(sqlString)
            util.logger.error(e)
            records = None

        self.currentCursor.connection.close()

        return records

    def getRowOnId(self, tableName, id):
        """
        Getting specific row from the table specified by its primary key (id)
        CONTRACT
          tableName (String): The name of the table to be queried
          id (Integer) : The primary key of the row to be returned
          RETURNS single table row
        """
        self.currentCursor = self.getDbCursor()
        
        sqlString = f'SELECT * FROM {tableName} WHERE id = {str(id)};'

        util.logger.debug(sqlString)

        try:
            record = self.currentCursor.execute(sqlString).fetchone()
        except Exception as e:
            util.logger.error(e)
            record = None

        self.currentCursor.connection.close()

        return record

    def getRowOnSpId(self, tableName, spid):
        """
        Getting specific row from the table specified by its Specify primary key (spid)
        CONTRACT
          tableName (String): The name of the table to be queried
          spid (Integer) : The Specify primary key of the row to be returned
          RETURNS single table row
        """
        self.currentCursor = self.getDbCursor()
        
        try:
            record = self.currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(spid)).fetchone()
        except Exception as e:
            util.logger.error(e)
            record = None

        self.currentCursor.connection.close()

        return record

    def deleteRowOnId(self, tableName, id):
        """
        Deleting specific row from the table specified by its primary key (id)
        CONTRACT
        tableName (String): The name of the table to be queried
        id (Integer) : The primary key of the row to be returned
        """
        self.currentCursor = self.getDbCursor()
        
        try:
            self.currentCursor.execute(f'DELETE FROM {tableName} WHERE id = {id};')
        except Exception as e:
            util.logger.error(e)
        
        self.currentCursor.connection.commit()
        self.currentCursor.connection.close()

    def getLastRow(self, table_name, collection_id):
        """
        Get the row from the specified table with the highest primary key (id)
        CONTRACT
          tableName (String): The name of the table to be queried
          RETURNS single table row (SQLITErow)
        """
        self.currentCursor = self.getDbCursor()

        sqlString = f'SELECT * FROM {table_name} WHERE id = (SELECT MAX(id) FROM {table_name} WHERE collectionid = {collection_id}) AND collectionid = {collection_id};'
        
        util.logger.debug(sqlString)

        try:
            record = self.currentCursor.execute(sqlString).fetchone()
        except Exception as e:
            util.logger.debug(sqlString)
            util.logger.error(e)
            raise e

        self.currentCursor.connection.close()
        
        return record

    def executeSqlStatement(self, sqlString):
        """
        Execute specified SQL statement
        CONTRACT
          sqlString (String) :
          RETURNS table rows as SqliteRow object list
        """

        self.currentCursor = self.getDbCursor()

        try:
            records = self.currentCursor.execute(sqlString).fetchall()
        except Exception as e:
            util.logger.debug(sqlString)
            util.logger.error(e)
            records = None

        self.currentCursor.connection.commit()
        self.currentCursor.connection.close()

        return records

    def getRowOnSpecifyId(self, tableName, id):
        """
        Getting specific row from the table specified by name using the primary key of the corresponding table in Specify
        CONTRACT
          tableName (String): The name of the table to be queried
          id (Integer) : The primary key of the row to be returned
          RETURNS single SqliteRow object from source table 
        """
        self.currentCursor = self.getDbCursor()
        record = self.currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
        self.currentCursor.connection.close()

        return record

    def getPrimaryKey(self, tableName, name, field='name'):
        """
        Function for fetching id (primary key) on name value
        CONTRACT 
           tableName (String): The name of the table to be queried
           name (String): The name of the 
        """
        # (tableName, {' %s = ' % field: '"%s"' % name})[0]['id']
        self.currentCursor = self.getDbCursor()
        sqlString = f'SELECT id FROM {tableName} WHERE {field} = {name};'
        record = self.currentCursor.execute(sqlString).fetchone()
        self.currentCursor.connection.close()
        return record

    def insertRow(self, tableName, fields):
        """
        Inserting a row made of field values into th table specified by name
        CONTRACT
            tableName (String): The name of the table to be queried
            fields (Dictionary) : A dictionary where the key is the field name and the value is the field value
                NOTE: Strings should be formatted with enclosing double quotation marks (")
                    Numbers should be formatted as strings
            RETURNS inserted record row
        """
        self.currentCursor = self.getDbCursor()
        fieldsString = []
        for key in fields:
            fieldsString.append(key)
        # fieldsString  = fieldsString[0:len(fieldsString)-2]
        # Jan thinks that joining the fieldString list is a cleaner solution.
        fieldsString = ','.join(fieldsString)
        sqlString = f"INSERT INTO {tableName} ({fieldsString}) VALUES ("
        sqlValues = []
        for key in fields:
            addSql = fields[key].replace('""', '')
            sqlValues.append(addSql)
            sqlValues = [item.replace('"', '') for item in sqlValues]

        valuesSql = '","'.join(sqlValues)
        valuesSql = f'"{valuesSql}")'
        sqlString = sqlString + valuesSql
        
        util.logger.debug('Inserting record using SQL: ', sqlString)
        
        self.currentCursor.execute(sqlString)
        self.currentCursor.connection.commit()

        recordID = self.currentCursor.lastrowid
        record = self.currentCursor.execute(f'SELECT * FROM {tableName} WHERE id = {str(recordID)}').fetchone()
        self.currentCursor.connection.close()

        return record

    def updateRow(self, tableName, recordID, values, where=''):
        """
        Updates a row made of field values in the table specified by name
        CONTRACT
          tableName (String)  : The name of the table to be queried
          recordID (int)      : The primary key of the record to be updated
          fields (Dictionary) : A dictionary where the key is the field name and the value is the field value
              NOTE: Strings should be formatted with enclosing double quotation marks (")
                    Numbers should be formatted as strings
          RETURNS updated record row
        """
        self.currentCursor = self.getDbCursor()
        fieldsString = ""

        for key in values:
            fieldsString += "%s, " % key

        if len(where) > 1:
            pass
        else:
            # Building the SQL query string below
            sqlStringPrepend = f"UPDATE {tableName} SET "
            sqlStringAppend = []

            for key in values:
                try:
                    val = values[key]
                    val = val.replace('"', '')
                    val = '"' + val + '"'
                    sqlString = f"{key} = {val}, "
                    sqlStringAppend.append(sqlString)

                except AttributeError:
                    sqlStringAppend.append(values[key])
            sqlStringLastPart = " WHERE id = {}".format(recordID)
            try:
                sqlAdd = ' '.join(sqlStringAppend)
                sqlAdd = sqlAdd[:-2]
                sqlStringFinal = sqlStringPrepend + ' ' + sqlAdd + sqlStringLastPart
            except TypeError:
                util.logger.error('TypeError occurred while constructing SQL for record update...')
                sqlStringFinal = ','.join(map(str, sqlStringAppend))

        
        util.logger.debug('Update record using SQL: ', sqlStringFinal)

        self.currentCursor.execute(sqlStringFinal)
        self.currentCursor.connection.commit()
        record = self.currentCursor.execute(f'SELECT * FROM {tableName} WHERE id = {str(recordID)}').fetchone()
        self.currentCursor.connection.close()

        return record

    def getFieldMap(self):
        """
        Get fields for a given DB API 2.0 cursor object that has been executed
        CONTRACT
          RETURNS a dictionary that maps each field name to a column index; 0 and up.
        """
        currentCursor = self.getDbCursor()
        results = {}
        column = 0
        for d in currentCursor.description:
            results[d[0]] = column
            column = column + 1
        self.currentCursor.connection.close()
        return results

    def getTableHeaders(self, tableName):
        """
        Get fields for a given DB API 2.0 cursor object that has been executed
        CONTRACT
           tableName
           
           RETURNS a dictionary that maps each field name to a column index; 0 and up.
        """
        self.currentCursor = self.getDbCursor()
        self.currentCursor.execute(f'SELECT * FROM {tableName} LIMIT 1')
        headers = list(map(lambda x: x[0], self.currentCursor.description))
        self.currentCursor.connection.close()
        return headers

    def loadSingleRecordFromSql(self, sql):
        """
        Retrieve single record from database based on sql query
        """
            
        util.logger.debug(sql)
        try:
            results = self.executeSqlStatement(sql)
        except Exception as e:
            util.logger.error(f"The SQL could not be executed - {e}\n Please check the Statement: \n{sql}")
            return None

        # If results returned then pick first one, otherwise set record to nothing 
        if len(results) > 0:
            record = results.pop()
            self.id = record[0]
        else: 
            record = None
        
        # NOTE: If no record retrieved None is returned 
        return record 
    