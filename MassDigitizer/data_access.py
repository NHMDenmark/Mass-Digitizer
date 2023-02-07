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
import logging
import sqlite3
from pathlib import Path

# Local imports
import PySimpleGUI as sg
import util

l = util.buildLogger('data_access')
logging.debug("IN data_access.py ---")

class DataAccess():

    def __init__(self, databaseName='db', do_in_memory=False):
        """
        Initialize for database access
            CONTRACT
               do_in_memory (boolean): Whether the database file should be run in-memory
        NOTE Database file is installed into user documents folder otherwise it would be readonly on a Windows PC in any case
        """
        logging.debug("Initializing Data Access module...")
        try:
            self.currentCursor = None  # Reset cursor pointer
            # Point to database file provided and connect
            self.filePath = util.getUserPath()

            self.dbFilePath = str(Path(self.filePath).joinpath(f'{databaseName}.sqlite3'))
        except Exception as e:
            logging.debug(e)

        logging.debug(('Connecting to database file: %s ...' % self.dbFilePath))

        try:
            self.connection = sqlite3.connect(self.dbFilePath)
        except Exception as e:
            # sg.popup_cancel(f"SQLite connection failed. Error: {e}")
            logging.debug("SQLite connection failed. Error: %s" % e)
            logError = f"The path {self.dbFilePath} does not exist."
            logging.debug(logError)
        self.connection.row_factory = sqlite3.Row

        try:
            self.currentCursor = self.connection.cursor()
        except Exception as e:
            sg.popup_cancel(f"Get the DB cursor error: {e}")
            logging.debug(e)

    def setDatabase(self, dbFileName='db'):
        """
        This optional function allows for setting a different database file like e.g. 'test'
          CONTRACT
            dbFileName (String): the name of the file excluding the extension '.sqlite3'
        """
        self.dbFilePath = str(Path(util.getUserPath()).joinpath(f'{dbFileName}.sqlite3'))
        logging.info("Database filepath: %s" % self.dbFilePath)

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
        # print(f'Connecting to db file: {self.dbFilePath} ...')
        self.connection = sqlite3.connect(self.dbFilePath)  # Normal user
        self.connection.row_factory = sqlite3.Row  # Enable column access by name: row['column_name']
        cursor = self.connection.cursor()
        # print('Connection established')
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
        # print(sqlString)

        if limit > 0:
            sqlString += f' LIMIT {limit}'
        logging.info('getRows() SQL : %s' % sqlString)
        try:
            records = currentCursor.execute(sqlString).fetchall()
        except Exception as e:
            logging.debug(e)
            pass
        self.currentCursor.connection.close()

        return records

    def getRowsOnFilters(self, tableName, filters, limit=10000, sort=None):
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
        currentCursor = self.getDbCursor()
        rowsOnFilterCall = f'-> getRowsONFilter({tableName}, {filters}, {limit})'
        logging.info("get rows on filter call= %s" % rowsOnFilterCall)
        sqlString = 'SELECT * FROM %s ' % tableName

        if filters.items():
            sqlString += "WHERE "
            for key, value in filters.items():
                sqlString += f'{key} {value} AND '
        sqlString = sqlString[0:len(sqlString) - 4]  # Remove trailing " AND "

        if sort is not None:
            sqlString += f' ORDER BY {sort}'

        if limit > 0:
            sqlString += f' LIMIT {limit}'

        logging.info("getRowsOnFilters SQL string : %s" % sqlString)

        records = currentCursor.execute(sqlString).fetchall()

        currentCursor.connection.close()
        # print(len(records))
        return records

    def getRowOnId(self, tableName, id):
        """
        Getting specific row from the table specified by its primary key (id)
        CONTRACT
          tableName (String): The name of the table to be queried
          id (Integer) : The primary key of the row to be returned
          RETURNS single table row
        """
        currentCursor = self.getDbCursor()
        record = currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
        currentCursor.connection.close()

        return record

    def getRowOnSpId(self, tableName, spid):
        """
        Getting specific row from the table specified by its Specify primary key (spid)
        CONTRACT
          tableName (String): The name of the table to be queried
          spid (Integer) : The Specify primary key of the row to be returned
          RETURNS single table row
        """
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
        currentCursor.execute(f'DELETE FROM {tableName} WHERE id = {id};')
        currentCursor.connection.commit()
        currentCursor.connection.close()

    def getMaxRow(self, tableName):
        """
        Get the row from the specified table with the highest primary key (id)
        CONTRACT
          tableName (String): The name of the table to be queried
          RETURNS single table row (SQLITErow)
        """
        currentCursor = self.getDbCursor()
        sql = f'SELECT MAX({tableName}.id) FROM {tableName};'
        record = currentCursor.execute(sql).fetchone()
        currentCursor.connection.close()
        # print(f'record: {record}')
        return record

    def executeSqlStatement(self, sql):
        """
        Execute specified sql statement
        CONTRACT
          sql (String) :
          RETURNS table rows as dictionary
        """
        message = f"Executing the following SQL: {sql}"
        logging.debug(message)
        self.currentCursor = self.getDbCursor()

        rows = self.currentCursor.execute(sql).fetchall()

        self.currentCursor.connection.commit()
        self.currentCursor.connection.close()

        return rows

    def getRowOnSpecifyId(self, tableName, id):
        """
        Getting specific row from the table specified by name using the primary key of the corresponding table in Specify
        CONTRACT
          tableName (String): The name of the table to be queried
          id (Integer) : The primary key of the row to be returned
          RETURNS single table row
        """
        self.currentCursor = self.getDbCursor()
        record = self.currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(id)).fetchone()
        self.currentCursor.connection.close()

        return record

    def getPrimaryKey(self, tableName, name, field='name'):
        """
        Function for fetching id (primary key) on name value
        """
        # (tableName, {' %s = ' % field: '"%s"' % name})[0]['id']
        currentCursor = self.getDbCursor()
        sql = f'SELECT id FROM {tableName} WHERE name = {name};'
        record = currentCursor.execute(sql).fetchone()
        currentCursor.connection.close()
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
        self.currentCursor.execute(sqlString)
        self.currentCursor.connection.commit()
        recordID = self.currentCursor.lastrowid
        record = self.currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(recordID)).fetchone()
        self.currentCursor.connection.close()

        return record

    def updateRow(self, tableName, recordID, values, where='', sqlString=None):
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
                # print('FINAL SQL is : ', sqlStringFinal)
            except TypeError:
                # print('IN sql build except typeError!')
                sqlStringFinal = ','.join(map(str, sqlStringAppend))

        self.currentCursor.execute(sqlStringFinal)
        self.currentCursor.connection.commit()
        record = self.currentCursor.execute("SELECT * FROM " + tableName + " WHERE id = " + str(recordID)).fetchone()
        self.currentCursor.connection.close()

        return record

    def getFieldMap(self):
        """
        Get fields for a given DB API 2.0 cursor object that has been executed
        CONTRACT
          cursor (Cursor) : Cursor object to be field mapped
          RETURNS a dictionary that maps each field name to a column index; 0 and up.
        """
        currentCursor = self.getDbCursor()
        results = {}
        column = 0
        for d in currentCursor.description:
            results[d[0]] = column
            column = column + 1

        return results

