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
import util
from models import model
from models import specimen
import data_access
import global_settings as gs

class RecordSet():#model.Model):
    """
    The recordset class is a representation of a set of specimen records allowing for easy navigation. 
    """

    def __init__(self, collection_id, range=3, specimen_id = 0):
      """
      Initialize (Constructor)
      """
      util.logger.debug(f'Initializing recordset with collection_id {collection_id}, range={range}, specimen_id={specimen_id}')

      self.collectionId = collection_id
      self.recordRange = range
      self.records = []
      
      self.db = data_access.DataAccess(gs.databaseName)

      self.headers = self.db.getTableHeaders('specimen')
      
      self.reLoad(specimen_id)
    
    def reLoad(self, specimen_id):
      """
      Sets the current specimen record and instance  
      """
      self.setCurrentSpecimen(specimen_id)
      self.load()

    def setCurrentSpecimen(self, specimen_id):
      """
      TODO Description / Contract
      """
      if specimen_id > 0:
        # if specimen record id specified fetch it as the current record in focus 
        specimenRecord = self.db.getRowOnId('specimen', specimen_id)
      else:
        # if no id is specified, fetch the latest record as the focus 
        specimenRecord = self.db.getMaxRow('specimen') 

      # Create specimen instance from record data 
      self.currentSpecimen = specimen.Specimen(self.collectionId)
      self.currentSpecimen.setFields(specimenRecord)

    def load(self):
      """
      Load adjacent records in range 
      """
      util.logger.debug(f'recordset: Load adjacent records in range. collectionId: {self.collectionId}, currentSpecimen id: {self.currentSpecimen.id}, range: {self.recordRange}')
      self.records = self.db.getRowsOnFilters('specimen',{
          'collectionid': f'={self.collectionId}',
          'id' : f'<={self.currentSpecimen.id}',
        }, limit=self.recordRange)
      

    def getAdjacentRecordList(self, tableHeaders):
      """
      TODO Explanation forthcoming
      """
      util.logger.debug(f'recordSet.getRecordList({tableHeaders})')

      # TODO Explain 
      recordList = [[row for row in line] for line in self.records]
      adjacentRecords = []  # the curated rows needed to populate the table
      #completeRowDicts = [] # full rows needed to populate the form
      for record in recordList:
        columnSet = dict(zip(self.headers, record))
        #completeRowDicts.append(columnSet)
        adjacentRecord = []
        for column in tableHeaders:
            recordRow = columnSet[column]
            adjacentRecord.append(recordRow)
        adjacentRecords.append(adjacentRecord)

      return adjacentRecords
  
      


      