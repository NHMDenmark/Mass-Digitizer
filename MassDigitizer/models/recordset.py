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
      
      self.setCardinalSpecimen(specimen_id)
      self.load()

    def setCardinalSpecimen(self, specimen_id):
      """
      TODO Description / Contract
      """
      if specimen_id > 0:
        # if specimen record id specified fetch it as the cardinal record in focus 
        specimenRecord = self.db.getRowOnId('specimen', specimen_id)
      else:
        # if no id is specified, fetch the latest record as the focus 
        specimenRecord = self.db.getLastRow('specimen', self.collectionId) 

      # Create specimen instance from record data 
      self.cardinalSpecimen = specimen.Specimen(self.collectionId)
      self.cardinalSpecimen.setFields(specimenRecord)

    def load(self):
      """
      Load adjacent records in range 
      """
      util.logger.debug(f'recordset: Load adjacent records in range. collectionId: {self.collectionId}, cardinalSpecimen id: {self.cardinalSpecimen.id}, range: {self.recordRange}')
      # Fetch records preceding cardinal record based on id within range specified  
      self.records = self.db.getRowsOnFilters('specimen',{
          'collectionid': f'={self.collectionId}',
          'id' : f'<={self.cardinalSpecimen.id}',
        }, limit=self.recordRange, sort='id', descending=True)
      util.logger.debug(f'loaded {len(self.records)} adjacent records...')
    
    def reload(self, specimen_record):
      """
      Sets new cardinal specimen and loads adjacent records based on it   
      """
      self.cardinalSpecimen = specimen.Specimen(self.collectionId)
      specimenId = 0
      if specimen_record is not None: 
        specimenId = specimen_record['id']
      self.setCardinalSpecimen(specimenId)

      self.load()

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
  

    def __str__ (self):
        return f'[{self.cardinalSpecimen}] id:{self.id}, name:{self.name}, fullname = {self.fullName}, specimennotes = {self.specimennotes}'      
