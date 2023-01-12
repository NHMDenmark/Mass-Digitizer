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

  PURPOSE: Represent taxon data record as "Model" in the MVC pattern  
"""

from datetime import datetime
import sys
from pathlib import Path

# Below line is needed for accessing internal dependencies for some fucking reason 
sys.path.append(str(Path(__file__).parent.parent.joinpath('')))

# Internal dependencies
import data_access
import global_settings as gs
import specify_interface

class Model:
    """
    The model class is a base class for data models inheriting & re-using a suite of shared functions
    """

    def __init__(self, collection_id):
        """
        Set up blank record instance for data entry on basis of collection id 
        """ 
        self.table          = 'model'
        self.sptype         = 'model' # NOTE not represented in Specify API
        self.id             = 0
        self.spid           = 0 
        self.gbifKey        = 0
        self.guid           = ''
        self.code           = ''
        self.name           = ''
        self.fullName       = ''
        self.parentFullName = ''
        self.parentId       = 0
        self.remarks        = ' '
        self.notes          = ''
        self.collectionId   = collection_id
        self.status         = 0
        self.source         = 'Unspecified'
        self.visible        = 0

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

            # print(f' - Updated {self.table} record with id: {self.id} and specify id: {self.spid} ')
        if self.id > 0:
            # Record Id is not 0 therefore existing record to be updated
            record = self.db.updateRow(self.table, self.id, self.getFieldsAsDict())
        else:
            # Record Id is 0 therefore existing record to be created
            record = self.db.insertRow(self.table, self.getFieldsAsDict())
            self.id = record['id']

        return record

    def load(self, id):
        """
        Function for loading and populating instance from database record  
        CONTRACT 
           id: Primary key of current record   
        """
        #print(f' - loading record with id: {id}')
        record = self.db.getRowOnId(self.table , id)
        if record is not None: 
            self.setFields(record)

    def delete(self):
        """
        Function for deleting database record belonging to current instance 
        CONTRACT 
           id: Primary key of current record   
        """
        # print(f' - deleting record with id: {self.id}')
        record = self.db.deleteRowOnId(self.table, self.id)

    def loadPrevious(self, id):
        """
        Function for loading previous object record data 
        CONTRACT
           id: Primary key of current record; If 0 then latest record    
           RETURNS record or None, if none retrieved 
        """

        # Construct query for extracting the previous record 
        sql = f'SELECT * FROM {self.table} s ' 
        # If existing record (id > 0) then fetch the one that has the highest lower id than current 
        if id > 0: 
            sql = sql + f"WHERE s.id < {id} " 
        # If blank record then fetch the one with the highest id 
        sql = sql + " ORDER BY s.id DESC LIMIT 1 "        
        # print(sql)

        # Fetch results from database
        try:
            results = self.db.executeSqlStatement(sql)
        except Exception as e:
            pass
            # print(f"The SQL could not be executed - {e}\n Please check the Statement: \n{sql}")
        # If results returned then pick first one, otherwise set record to nothing 
        if len(results) > 0:
            record = results[0]
        else: 
            record = None

        # If record retrieved set fields 
        if record:
            self.setFields(record)
        
        # NOTE: If not record retrieved None is returned 
        return record 
    
    def loadNext(self, id):
        """
        Function for loading next object record data, if any 
        CONTRACT
           id: Primary key of current record; If 0 then latest record    
           RETURNS record or None, if none retrieved  
        """

        # Construct query for extracting the previous record 
        sql = f"SELECT * FROM {self.table} s " 
        # If existing record (id > 0) then fetch the one that has the lowest higher id than current 
        if id > 0: 
            sql = sql + f"WHERE s.id > {id} " 
        # If blank record then fetch the one with the highest id 
        sql = sql + " ORDER BY s.id LIMIT 1 "        
        # print(sql)

        # Fetch results from database
        try:
            results = self.db.executeSqlStatement(sql)
        except Exception as e:
            pass
            # print(f"The SQL could not be executed - {e}\n Please check the Statement: \n{sql}")
        # If results returned then pick first one, otherwise set record to nothing 
        if len(results) > 0:
            record = results[0]
        else: 
            record = None

        # If record retrieved set fields 
        if record:
            self.setFields(record)
        
        # NOTE: If not record retrieved None is returned 
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
                'name':f'"{self.name}"',
                'fullname':f'"{self.fullName}"',
                'parentfullname':f'"{self.parentFullName}"',
                'collectionid':f'{self.collectionId}',
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
        self.name = record['name']
        self.fullName = record['fullname']
        #self.parentfullname = record['parentfullname']
        pass

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

    def __str__ (self):
        return f'[{self.table}] id:{self.id}, name:{self.name}, fullname = {self.fullName}, notes = {self.notes}'
