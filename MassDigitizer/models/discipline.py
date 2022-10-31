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

  PURPOSE: Represent discipline data record as "Model" in the MVC pattern  
"""

from datetime import datetime

# Internal dependencies
from models import model
import data_access as db
import global_settings as gs
import specify_interface as sp

class Discipline(model.Model):
    "Class representing ... "

    def __init__(self, collectionId) -> None:
        # Set up blank record 
        self.table   = 'discipline'
        self.sptype  = 'discipline'
        self.spid = 0
        self.id = 0
        self.name = ''
        self.fullname = ''
        self.taxontreedefid = 0

    def fill(self, specifyObject):
        self.spid = specifyObject['id']
        self.name = specifyObject['name']
        #self.fullname = specifyObject['collectionname']
        self.taxontreedefid = specifyObject['taxontreedef'].split('/')[4]
        print(f'Taxon tree def ID: {self.taxontreedefid}')

        #self.
    
    def __str__ (self):
        return f'[{self.table}] id:{self.id}, spid:{self.spid}, name:{self.name}'
