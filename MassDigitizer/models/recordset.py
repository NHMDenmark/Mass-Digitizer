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

  PURPOSE: Represent specimen record set as "Model" in the MVC pattern  
"""

# Internal dependencies
from models import model
from models import specimen
import data_access
import global_settings as gs

class recordset(model.Model):
    """
    The recordset class is a representation of a set of specimen records allowing for easy navigation. 
    """

    def __init__(self, collection_id, range=3, specimen_id = 0):
      """
      Initialize (Constructor)
      """
      self.collectionId = collection_id
      self.recordRange = range
      
      self.db = data_access.DataAccess(gs.databaseName)
      
      if specimen_id > 0:
        specimenRecord = self.db.getRowOnId('specimen', specimen_id)
        self.currentSpecimen = specimen.specimen(self.collectionId). self.db.getRowOnId('specimen', specimen_id)
      else:
        self.currentSpecimen = None 

    def load(self):
      """
      Load adjacent records in range 
      """

      records = self.db.getRowsOnFilters('specimen',{
          'collectionid': f'={self.collectionId}',
          'id' : f'<={self.currentSpecimen}',
        }, limit=self.recordRange)


      pass