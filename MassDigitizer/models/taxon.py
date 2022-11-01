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
        self.rankid    = 0
        self.author    = ''
        self.parentid  = 0

        self.institutionId   = gs.institutionId #db.getRowOnId('collection',collection_id)['institutionid']
        self.collectionId    = collection_id

    # Base functions covered in [Model] parent class 
    #def save(self): pass
    #def load(self, id): pass
    #def loadPrevious(self, id): pass
    #def loadNext(self, id): pass
    
    def setFields(self, record):
        pass

    def getFieldsAsDict(self):
        pass
    
    def fill(self, specifyObject):
        self.id = specifyObject['id']
        self.name = specifyObject['name']
        self.fullname = specifyObject['fullname']
        self.rankid = specifyObject['rankid']
        self.author = specifyObject['author']
        
        self.parentid = specifyObject['parent'].split('/')[4]
        self.parent = None

    def loadPredefinedData(self):
        pass

    def getParent(self, token):
        self.parent = Taxon(self.collectionId)
        self.parent.fill(sp.getSpecifyObject(self.sptype, self.parentid, token))
        return self.parent 

    def getParentage(self, token):
        # 
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
