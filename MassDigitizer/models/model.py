# -*- coding: utf-8 -*-
"""
  Created on September 28, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Generic base class "Model" in the MVC pattern
"""

import os
import sys

# Internal dependencies
import global_settings as gs
import specify_interface
import util
import data_access

# TODO Explain reason for below code
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class Model:
    """
    The model class is a base class for data models inheriting & re-using a suite of shared functions
    """

    def __init__(self, collection_id):
        """
        Set up blank record instance for data entry on basis of collection id
        """
        self.table = 'model'
        self.sptype = 'model'  # NOTE not represented in Specify API
        self.id = 0
        self.spid = 0
        self.gbifKey = 0
        self.dasscoid = ''
        self.guid = ''
        self.code = ''
        self.name = ''
        self.author = ''
        self.fullName = ''
        self.rankName = ''
        self.parentFullName = ''
        self.parentId = 0
        self.familyName = ''  # TODO Too specific! Solve in a different way ...
        self.idNumber = '' # TODO Too specific! Solve in a different way ...
        self.remarks = ' '
        self.notes = ''
        self.collectionId = collection_id
        self.status = 0
        self.source = 'Unspecified'
        self.visible = 0

        # Enable usage as autosuggestobject
        self.treedefid = 0
        self.rankid = 0

        #
        self.db = data_access.DataAccess(gs.databaseName)
        self.sp = specify_interface.SpecifyInterface()

    # Generic local database interfacing functions

    def save(self):
        """
        Function telling instance to save its data either as a new record (INSERT) or updating an existing one (UPDATE)
        Data to be saved is retrieved from self as a dictionary with the object table headers as 'keys' and the form field content as 'values'.
        CONTRACT
           RETURNS database record
        """

        # Checking if Save is a novel record, or if it is updating existing record.
        if self.id > 0:
            # Record Id is not 0 therefore existing record to be updated
            record = self.db.updateRow(self.table, self.id, self.getFieldsAsDict())
        else:
            # Record Id is 0 therefore existing record to be created
            record = self.db.insertRow(self.table, self.getFieldsAsDict())
            self.id = record['id']

        return record

    def load(self, id=0):
        """
        Function for loading and populating instance from database record
        CONTRACT
           id: Primary key of current record. If zero then instance id is checked otherwise nothing is loaded.
            RETURNS: Record as SqliteRow object
        """

        if id == 0: id = self.id

        record = self.db.getRowOnId(self.table, id)

        if record is not None:
            self.setFields(record)

        return record

    def refresh(self):
        """
        TODO Function contract
        """
        return self.load(self, self.id)

    def delete(self):
        """
        Function for deleting database record belonging to current instance
        CONTRACT
           id: Primary key of current record
        """

        record = self.db.deleteRowOnId(self.table, self.id)

    def loadPrevious(self):
        """
        Function for loading previous object record data
        on the basis of the current primary key, if any.
        CONTRACT
           RETURNS record or None, if none retrieved
        """
        id = self.id # primary key is encapsulated by model itself 
        if not id:
            id = 0
        else:
            id = int(id)

        # Construct query for extracting the previous record
        sql = f'SELECT * FROM {self.table} s '

        # If existing record (id > 0) then fetch the one that has the highest lower id than current
        if id > 0:
            sql = sql + f"WHERE s.id < {id} "
        else:
            # Blank record: Fetch the one with the highest id
            sql = sql + f"WHERE s.id = (SELECT MAX(id) FROM {self.table} WHERE s.collectionid = {self.collectionId}) "

        sql = sql + f"AND s.collectionid = {self.collectionId} "  # Filter on current collection
        #sql = sql + "LIMIT 1; "

        record = self.db.loadSingleRecordFromSql(sql)
        if record is not None:
            self.setFields(record)
        
        return record

    def loadNext(self):
        """
        Function for loading next object record data, if any
        CONTRACT
           RETURNS record or None, if none retrieved
        """
        id = self.id # primary key is encapsulated by model itself
        
        # If existing record (id > 0) then fetch the one that has the lowest higher id than current

        # Construct query for extracting the previous record
        sql = f"SELECT * FROM {self.table} s "
        if id > 0:
            sql = sql + f"WHERE s.id > {id} "
        else:
            # Blank record: No going forward
            util.logger.debug('Attempt to forward on blank record')
            return None

        sql = sql + f" AND s.collectionid = {self.collectionId}"  # Filter on current collection
        # Sort on ID to get the latest record out
        sql = sql + " ORDER BY s.id LIMIT 1;"
        record = self.db.loadSingleRecordFromSql(sql)
        record
        if record is not None:
            self.setFields(record)
        return record

    def loadOnFullname(self, fullname, collection_id):
        """
        Retrieves data and fills instance based on fullname field
        CONTRACT
            fullname (String)   : fullname field to searched on
            collection_id (Int) : primary key of collection to be filtered on
        """
        records = self.db.getRowsOnFilters(self.table, {'fullname': f'={fullname}', 'collectionid': f'{collection_id}'},1)
        if len(records) > 0:
            record = records[0]
            self.setFields(record)
        else:
            record = None

        return record

    # Functions fully implemented in inheriting classes

    def loadPredefinedData(self):
        """
        Generic function for loading predefined data in order to get primary keys and other info to be pooled at selection in GUI
        NOTE Implemented in inheriting classes.
        """
        pass

    def getFieldsAsDict(self):
        """
        Generic function that generates and returns a dictonary with database column names as keys and the instance's fields as values for passing on to data access handler
        NOTE Fully implemented in inheriting classes
        """

        fieldsDict = {
            'name': f'"{self.name}"',
            'fullname': f'"{self.fullName}"',
            'parentfullname': f'"{self.parentFullName}"',

            'collectionid': f'{self.collectionId}',
            'treedefid': f'{self.treedefid}',
            'rankid': f'{self.rankid}',
        }

        return fieldsDict

    def setFields(self, record):
        """
        Function for setting base object data field from record
        CONTRACT
           record: sqliterow object containing record data
        NOTE Fully implemented in inheriting classes
        """

        self.id = record['id']
        self.spid = record['spid']
        self.name = record['name']
        self.author = record['author']
        self.fullName = record['fullname']
        self.parentFullName = record['parentfullname']
        self.collectionId = record['collectionid']
        self.treedefid = record['treedefid']
        self.rankid = record['rankid']
        self.idNumber = record['idnumber']

    # Specify Interfacing functions

    def fetch(self, token, spid=0):
        """
        Generic function for fetching a data record from Specify API and passing it to the fill(...)-function
        CONTRACT
            token (String)  : CSFR token needed for accessing the Specify API
            id (Integer)    : Primary key of the object in question
        NOTE Implemented in inheriting classes.
        """
        if spid == 0: spid = self.spid
        #
        jsonObject = self.sp.getSpecifyObject(self.sptype, spid, token)
        #
        self.fill(jsonObject)

    def fill(self, jsonObject, source="Specify"):
        """
        Function for filling model's fields with data from record fetched from external source
        CONTRACT
            jsonObject (json)  : Data record fetched from external source
            source (String)    : String describing external source.
                                 Options:
                                     "Specify = "Specify API
        """
        self.spid = jsonObject['id']
        self.name = jsonObject['name']
        self.fullName = jsonObject['fullname']

    def getParent(self, specify_interface):
        """
        Generic function for fetching current instance's parent record
        CONTRACT
            specify_interface TODO
        NOTE Implemented in inheriting classes
        """
        pass

    def getParentage(self, specify_interface):
        """
        Generic function for recursively fetching the entire parentage tree for current instance
        CONTRACT
            specify_interface TODO
        NOTE Implemented in inheriting classes
        """
        pass

    # Generic functions

    def __str__(self):
        return f'[{self.table}] id:{self.id}, name:{self.name}, fullname = {self.fullName}, notes = {self.notes}'
