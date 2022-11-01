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
import data_access as db
import global_settings as gs
import specify_interface as sp

class Collection(model.Model):
    "Class representing ... "

    def __init__(self, collection_id) -> None:
        # Set up blank record 
        model.Model.__init__(self, collection_id)
        self.table   = 'collection'
        self.sptype  = 'collection'
        self.discipline = None 

        # Predefined data fields
        self.storageLocations = None 
        self.prepTypes = None 
        self.typeStatuses = None 
        self.geoRegions = None 
        self.geoRegionSources = None 

        #self.loadPredefinedData() # TODO Turned off for now until needed 

    def fill(self, specifyObject, token):
        self.spid = specifyObject['id']
        self.id = 0
        self.guid = specifyObject['guid']
        self.name = specifyObject['collectionname']
        #self.fullname = specifyObject['collectionname'] 
        disciplineId = int(specifyObject['discipline'].split('/')[4])
        self.fetchDiscipline(disciplineId, token)
    
    def fetchDiscipline(self, disciplineId, token):
        """
        
        """
        self.discipline = discipline.Discipline(self.id)
        disciplineObj = sp.getSpecifyObject('discipline', disciplineId, token)
        self.discipline.fill(disciplineObj)

    def loadPredefinedData(self):
        """
        Function for loading predefined data in order to get primary keys and other info to be pooled at selection in GUI 
        """
        self.storageLocations = db.getRowsOnFilters('storage', {'collectionid =': f'{self.collectionId}'})
        self.prepTypes = db.getRowsOnFilters('preptype', {'collectionid =': f'{self.collectionId}'})
        self.typeStatuses = db.getRowsOnFilters('typestatus', {'collectionid =': f'{self.collectionId}'})
        self.geoRegions = db.getRowsOnFilters('georegion', {'collectionid =': f'{self.collectionId}'}) 
        self.geoRegionSources = db.getRowsOnFilters('georegionsource', {'collectionid =': f'{self.collectionId}'}) 

        