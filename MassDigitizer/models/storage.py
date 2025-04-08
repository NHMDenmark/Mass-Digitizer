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
import data_access
import global_settings as gs
import specify_interface

db = data_access.DataAccess(gs.databaseName)
sp = specify_interface.SpecifyInterface()

class Storage(model.Model):
    """
     The storage class is a representation of a storage record to hold its data
     Any instance is either an existing record in the database or transient pending an insert
"""

    def __init__(self, collection_id) -> None:
        # Set up blank record
        model.Model.__init__(self, collection_id)
        self.table = 'storage'
        self.sptype = 'storage'
        self.discipline = None
        self.collectionid = collection_id
        self.name = ''
        self.fullName = ''
        self.spid = 0



        # self.loadPredefinedData() # TODO Turned off for now until needed


    def getFieldsAsDict(self):
        """
        Generates a dictonary with database column names as keys and specimen records fields as values
        RETURNS said dictionary for passing on to data access handler
        """

        fieldsDict = {
            'id': f'"{self.id}"',
            'spid': f'"{self.spid}"',
            'guid': f'"{self.guid}"',
            'name': f'"{self.name}"',
            'fullname': f'"{self.fullName}"',
            'collectionid': f'"{self.collectionid}"'
        }

        return fieldsDict

    def setFields(self, record):
        """
        Function for setting specimen data field from record
        CONTRACT
           record: sqliterow object containing specimen record data
        """
        # model.Model.setFields(self, record)
        self.id = record['id']
        self.spid = record['spid']
        self.guid = record['guid']
        self.name = record['name']
        self.fullName = record['fullname']
        self.collectionId = record['collectionid']

    def loadPredefinedData(self):
        pass

    def fill(self, specifyObject, token):
        """
        Function for filling storage model's fields with data from record fetched from external source
        CONTRACT 
            jsonObject (json)  : Data record fetched from external source
            source (String)    : String describing external source. 
                                 Options:
                                     "Specify = "Specify API 
        """
        self.spid = specifyObject['id']
        self.id = 0
        self.guid = specifyObject['guid']
        self.name = specifyObject['name']
        self.fullName = specifyObject['fullname']
        # disciplineId = int(specifyObject['discipline'].split('/')[4])
        # self.fetchDiscipline(disciplineId, token)


    def loadPredefinedData(self):
        """
        Function for loading predefined data in order to get primary keys and other info to be pooled at selection in GUI
        """
        self.storageLocations = db.getRowsOnFilters('storage', {'collectionid =': f'{self.collectionId}'})
        self.prepTypes = db.getRowsOnFilters('preptype', {'collectionid =': f'{self.collectionId}'})
        self.typeStatuses = db.getRowsOnFilters('typestatus', {'collectionid =': f'{self.collectionId}'})
        self.geoRegions = db.getRowsOnFilters('georegion', {'collectionid =': f'{self.collectionId}'})
        #self.geoRegionSources = db.getRowsOnFilters('georegionsource', {'collectionid =': f'{self.collectionId}'})

    def getParent(self, token):
        pass

    def getParentage(self, token):
        # Recursive function for constructing the entire parent sequence down to "Life"
        pass

    def __str__ (self):
        return f'id:{self.id}, spid:{self.spid}, name:{self.name}, fullname:{self.fullName}'
