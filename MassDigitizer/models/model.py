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

# Internal dependencies
import data_access as db
import global_settings as gs
import specify_interface as sp

class Model:
    """
    The model class is a base class for data models inheriting & re-using a suite of shared functions
    """

    def __init__(self, collection_id):
        """
        Set up blank record instance for data entry on basis of collection id 
        """ 
        self.table    = 'model'
        self.sptype   = 'model' # NOTE not represented in Specify API
        self.id       = 0
        self.spid     = 0 
        self.guid     = ''
        self.code     = ''
        self.name     = ''
        self.fullname = ''
    
    def save(self):
        """
        Function telling instance to save its data either as a new record (INSERT) or updating an existing one (UPDATE)
        Data to be saved is retrieved from self as a dictionary with the object table headers as 'keys' and the form field content as 'values'.        
        CONTRACT 
           RETURNS database record 
        """

        # Checking if Save is a novel record , or if it is updating existing record.
        if self.id > 0:
            # Record Id is not 0 therefore existing record to be updated 
            print(f' - Update {self.table} record with id: ', self.id)
            record = db.updateRow(self.table, self.id, self.getFieldsAsDict())
        else:
            # Record Id is not 0 therefore existing record to be updated 
            print(f' - Insert new {self.table} record with id: ', self.id)
            record = db.insertRow(self.table, self.getFieldsAsDict())
            self.id = record['id']

        return record

    def load(self, id):
        """
        Function for loading and populating instance from database record  
        CONTRACT 
           id: Primary key of current record   
        """
        #print(f' - loading record with id: {id}')
        record = db.getRowOnId(self.table , id)
        if record is not None: 
            self.setFields(record)

    def delete(self):
        """
        Function for deleting database record belonging to current instance 
        CONTRACT 
           id: Primary key of current record   
        """
        print(f' - deleting record with id: {self.id}')
        record = db.deleteRowOnId(self.table, self.id)
    
    def setFields(self, record):
        """
        Function for setting base object data field from record 
        CONTRACT 
           record: sqliterow object containing record data 
        """

        self.id = record['id']
        self.name = record['name']
        self.fullname = record['fullname']
        
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
        print(sql)

        # Fetch results from database
        results = db.executeSqlStatement(sql)

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
        print(sql)

        # Fetch results from database
        results = db.executeSqlStatement(sql)

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

    def getFieldsAsDict(self):
        """
        Generic function that generates and returns a dictonary with database column names as keys and the instance's fields as values for passing on to data access handler
        NOTE Implemented in inheriting classes 
        """
        pass
    
    def loadPredefinedData(self):
        """
        Generic function for loading predefined data in order to get primary keys and other info to be pooled at selection in GUI 
        NOTE Implemented in inheriting classes. 
        """
        pass
    
    def fetch(self, token, id=0):
        """
        Generic function for fetching a data record from Specify API and passing it to the fill(...)-function
        CONTRACT 
            token (String)  : CSFR token needed for accessing the Specify API 
            id (Integer)    : Primary key of the object in question 
        NOTE Implemented in inheriting classes. 
        """
        if id == 0: id = self.id
        #
        specifyObject = sp.getSpecifyObject(self.sptype, id, token)
        #
        self.fill(specifyObject)

    def fill(self, specifyObject):
        """
        Generic function for filling model's fields with data record fetched from Specify API 
        CONTRACT 
            specifyObject (json)  : Specify data record fetched from Specify API 
        NOTE Implemented fully in inheriting classes.         
        """
        self.spid = specifyObject['id']
        self.name = specifyObject['name']
        self.fullname = specifyObject['fullname']

    def getParent(self):
        """
        Generic function for fetching current instance's parent record 
        NOTE Implemented in inheriting classes 
        """        
        pass

    def getParentage(self):
        """
        Generic function for recursively fetching the entire parentage tree for current instance 
        NOTE Implemented in inheriting classes 
        """        
        pass

    def loadPredefinedData(self):
        """
        Function for loading predefined data in order to get primary keys and other info to be pooled at selection in GUI 
        NOTE Implemented in inheriting classes 
        """
        pass

    def __str__ (self):
        return f'[{self.table}] id:{self.id}, name:{self.name}, fullname = {self.fullname}'