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
from models import model
import data_access as db
import global_settings as gs
import specify_interface as sp

class Taxon(model.Model):
    """
    The taxon class is a representation of a taxon record to hold its data
    Any instance is either an existing record in the database or transient pending an insert
    """

    def __init__(self, collection_id):
        """Set up blank taxon"""         
        model.Model.__init__(self, collection_id)
        self.table     = 'taxon'
        self.sptype    = 'taxon'
        self.author    = ''
        self.rankid    = 0
        self.parentid  = 0

        self.institutionId   = gs.institutionId #db.getRowOnId('collection',collection_id)['institutionid']
        self.collectionId    = collection_id

    def getFieldsAsDict(self):
        """
        Generates a dictonary with database column names as keys and specimen records fields as values 
        RETURNS said dictionary for passing on to data access handler 
        """
        
        fieldsDict = {
                'spid':f'"{self.spid}"', 
                'guid':f'"{self.guid}"',
                'name':f'"{self.name}"',
                'fullname':f'"{self.fullname}"',
                'author':f'"{self.author}"',
                'remarks':f'"{self.remarks}"',
                'rankid':f'"{self.rankid}"',
                'parentid':f'"{self.parentid}"',
                }
        
        return fieldsDict
     
    def setFields(self, record):
        """
        Function for setting specimen data field from record 
        CONTRACT 
           record: sqliterow object containing specimen record data 
        """
        #model.Model.setFields(self, record)
        self.id = record['id']
        self.spid = record['spid']
        self.guid = record['guid']
        self.name = record['name']
        self.fullname = record['fullname']
        self.author = record['author']
        self.remarks = record['remarks']
        self.rankid = record['rankid']        
        self.parentid = record['parentid']
        self.parent = None
   
    def fill(self, specifyObject):
        self.spid = specifyObject['id'] # NOTE The 'id' of the Specify Object corresponds to the 'spid' field in the local app db
        self.guid = specifyObject['guid']
        self.name = specifyObject['name']
        self.fullname = specifyObject['fullname']
        self.author = specifyObject['author']
        self.remarks = specifyObject['remarks']
        self.rankid = specifyObject['rankid']        
        self.parentid = specifyObject['parent'].split('/')[4]
        self.parent = None

    def loadPredefinedData(self):
        pass

    def getParent(self, token):
        self.parent = Taxon(self.collectionId)
        self.parent.fill(sp.getSpecifyObject(self.sptype, self.parentid, token))
        return self.parent 

    def getParentage(self, token):
        # Recursive function for constructing the entire parent sequence down to "Life"
        done = False 
        current = self 
        while done != True: 
            temporary = current.getParent() 
            if (temporary.name == 'Life'): 
                done = True
            else: 
                current = temporary

    def __str__ (self):
        return f'id:{self.id}, name:{self.name}, fullname:{self.fullname}, author:{self.author}, rankid:{self.rankid}, parentid: {self.parentid} '
