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

  PURPOSE: Represent collection data record as "Model" in the MVC pattern  
"""

from datetime import datetime

# Internal dependencies
from models import model
from models import discipline
#import data_access
import global_settings as gs
#import specify_interface

class Collection(model.Model):
    """
    Class representing a collection data record  
    """

    def __init__(self, collection_id) -> None:
        # Set up blank record 
        model.Model.__init__(self, collection_id)
        self.table          = 'collection'
        self.sptype         = 'collection'
        self.institutionId  = 0
        self.taxonTreeDefId = 0
        self.disciplineId   = 0
        self.discipline     = None 

        # Predefined data fields
        self.storageLocations = None 
        self.prepTypes = None 
        self.typeStatuses = None 
        self.geoRegions = None 
        self.geoRegionSources = None 

        self.load(collection_id)

        #self.loadPredefinedData() # TODO Turned off for now until needed 
        pass

# Overriding inherited functions

    def loadPredefinedData(self):
        """
        Function for loading predefined data in order to get primary keys and other info to be pooled at selection in GUI 
        """
        self.storageLocations = self.db.getRowsOnFilters('storage', {'collectionid =': f'{self.collectionId}'})
        self.prepTypes = self.db.getRowsOnFilters('preptype', {'collectionid =': f'{self.collectionId}'})
        self.typeStatuses = self.db.getRowsOnFilters('typestatus', {'collectionid =': f'{self.collectionId}'})
        self.geoRegions = self.db.getRowsOnFilters('georegion', {'collectionid =': f'{self.collectionId}'}) 
        self.geoRegionSources = self.db.getRowsOnFilters('georegionsource', {'collectionid =': f'{self.collectionId}'}) 
   
    def getFieldsAsDict(self):
        """
        Generates a dictonary with database column names as keys and specimen records fields as values 
        RETURNS said dictionary for passing on to data access handler 
        """
        
        fieldsDict = {
                'id':               f'{self.id}', 
                'spid':             f'{self.spid}', 
                'name':             f'"{self.name}"', 
                'institutionid':    f'{self.institutionId}', 
                'taxontreedefid':   f'{self.taxonTreeDefId}', 
                'visible':          f'{self.visible}', 
                }
        
        return fieldsDict

    def setFields(self, record):
        """
        Function for setting collection object data field from record 
        CONTRACT 
           record: sqliterow object containing record data 
        """

        self.id             = record['id']
        self.spid           = record['spid']
        self.name           = record['name']
        self.institutionId  = record['institutionid']
        self.taxonTreeDefId = record['taxontreedefid']
        self.visible        = record['visible']      

# Specify Interfacing functions 

    def fill(self, jsonObject, source="Specify"):
        """
        Function for filling collection model's fields with data record fetched from external source
        CONTRACT 
            jsonObject (json)  : Data record fetched from external source
            source (String)    : String describing external source. 
                                 Options:
                                     "Specify = "Specify API 
        """
        self.source = source
        if jsonObject:
            if source=="Specify":
                self.spid = jsonObject['id']
                self.id = 0
                self.guid = jsonObject['guid']
                self.name = jsonObject['collectionname']
                #self.fullname = jsonObject['collectionname'] 
                self.disciplineId = int(jsonObject['discipline'].split('/')[4])
                #self.fetchDiscipline(disciplineId, token)
        else:
            self.remarks = 'Could not set values, because empty object was passed. '
            print('jsonObject EMPTY!!!')

    # Collection class specific functions 

    # def fetchDiscipline(self, disciplineId, token):
    #     """
    #     
    #     """
    #     self.discipline = discipline.Discipline(self.id)
    #     disciplineObj = self.sp.getSpecifyObject('discipline', disciplineId, token)
    #     self.discipline.fill(disciplineObj)

# Generic functions

    def __str__ (self):
        return f'[{self.table}] id:{self.id}, spid:{self.spid}, name:{self.name}, taxontreedefid = {self.taxonTreeDefId}'        