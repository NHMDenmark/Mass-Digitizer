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
from models import discipline
import data_access as db
import global_settings as gs
import specify_interface as sp

class Collection(model.Model):
    "Class representing ... "

    def __init__(self, collectionId) -> None:
        # Set up blank record 
        self.table   = 'collection'
        self.sptype  = 'collection'
        self.spid = 0
        self.id = 0
        self.guid = ''
        self.name = ''
        self.fullname = ''
        self.discipline = None 

    def fill(self, specifyObject, token):
        self.spid = specifyObject['id']
        self.id = 0
        self.guid = specifyObject['guid']
        self.name = specifyObject['collectionname']
        #self.fullname = specifyObject['collectionname']
        self.discipline = discipline.Discipline(self.id)
        disciplineId = int(specifyObject['discipline'].split('/')[4])
        disciplineObj = sp.getSpecifyObject('discipline', disciplineId, token)
        self.discipline.fill(disciplineObj)

        #self.
    
    def fetchDiscipline(self):
        pass
        