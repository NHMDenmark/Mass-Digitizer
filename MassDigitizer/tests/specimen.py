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

  PURPOSE: Represent specimen data record as "Model" in the MVC pattern  
"""

from datetime import datetime

# Internal dependencies
import data_access as db
import global_settings as gs

class specimen:
    # The specimen class is a representation of a specimen record to hold its data
    # Any instance is either an existing record in the database or transient pending an insert

    def __init__(self, collection_id):
        # Set up blank specimen for data entry on basis of collection id 
        self.id              = 0
        self.catalogNumber   = ''
        self.multiSpecimen   = 'False'
        self.taxonName       = ''
        self.taxonNameid     = 0
        #self.taxonspid 
        self.typeStatusName  = ''
        self.typeStatusId    = 0
        self.geoRegionName   = ''
        self.geoRegionId     = 0
        self.storageFullName = ''
        self.storageName     = ''
        self.storageId       = 0
        self.prepTypeName    = ''
        self.prepTypeId      = 0
        self.notes           = ''
        self.institutionId   = gs.institutionId #db.getRowOnId('collection',collection_id)['institutionid']
        self.collectionId    = collection_id
        self.userName        = gs.spUserName
        self.userId          = gs.spUserId
        self.workStation     = ''
        self.recordDateTime  = str(datetime.now())
        self.exported        = 0
        self.exportDateTime  = ''
        self.exportUserId    = ''

        self.loadPredefinedData()
    
    def loadPredefinedData(self):
        # Function for loading predefined data in order to get primary keys and other info to be pooled at selection in GUI 
        self.storageLocations = db.getRowsOnFilters('storage', {'collectionid =': f'{self.collectionId}'})
        self.prepTypes = db.getRowsOnFilters('preptype', {'collectionid =': f'{self.collectionId}'})
        self.typeStatuses = db.getRowsOnFilters('typestatus', {'collectionid =': f'{self.collectionId}'})
        self.geoRegions = db.getRowsOnFilters('georegion', {'collectionid =': f'{self.collectionId}'}) 
        self.geoRegionSources = db.getRowsOnFilters('georegionsource', {'collectionid =': f'{self.collectionId}'}) 
    
    def save(self):
        # Function telling instance to save its data either as a new record (INSERT) or updating an existing one (UPDATE)
        # Data to be saved is retrieved from self as a dictionary with ->
        #   the specimen table headers as 'keys' and the form field content as 'values'.        
        # CONTRACT 
        #   RETURNS record id (primary key)
        
        print('Saving specimen...')
        
        # Checking if Save is a novel record , or if it is updating existing record.
        if self.id > 0:
            # Record Id is not 0 therefore existing record to be updated 
            print('Update specimen record with id: ', self.id)
            record = db.updateRow('specimen', self.id, self.getFieldsAsDict())
        else:
            # Record Id is not 0 therefore existing record to be updated 
            print('Insert new specimen record.')
            record = db.insertRow('specimen', self.getFieldsAsDict())
            self.id = record['id']

        return self.id

    def load(self, id):
        # Function for loading and populating instance from database record  
        # CONTRACT 
        #   id: Primary key of current record; If 0 then latest record   
        
        record = db.getRowOnId(id)
        self.setFields(record)

    def setFields(self, record):
        # Function for setting specimen data field from record
        # CONTRACT
        #   record: sqliterow object containing record data

        self.id = record['id']
        self.catalogNumber = record['catalognumber']
        self.multiSpecimen = record['multispecimen']
        self.taxonName = record['taxonname']
        self.taxonNameid = record['taxonnameid']
        #self.taxonspid = record['taxonspid']
        self.typeStatusName = record['typestatusname']
        self.typeStatusId = record['typestatusid']
        self.geoRegionName = record['georegionname']
        self.geoRegionId = record['georegionid']
        self.storageFullName = record['storagefullname']
        self.storageName = record['storagename']
        self.storageId = record['storageid']
        self.prepTypeName = record['preptypename']
        self.prepTypeId = record['preptypeid']
        self.notes = record['notes'] 
        self.institutionId = record['institutionid']
        self.collectionId = record['collectionid']
        self.userName = record['username']
        self.userId = record['userid']
        self.workStation = record['workstation']
        self.recordDateTime = record['recorddatetime']
        self.exported = record['exported']
        self.exportDateTime = record['exportdatetime']
        self.exportUserId = record['exportuserid']

        self.loadPredefinedData()

    def loadPrevious(self, id):
        # Function for loading previous specimen record data 
        # CONTRACT
        #   id: Primary key of current record; If 0 then latest record    
        #   RETURNS record or None, if none retrieved 

        # Construct query for extracting the previous record 
        sql = "SELECT * FROM specimen s " 
        # If existing record (id > 0) then fetch the one that has a lower id than current which is also the highest 
        if id > 0: 
            sql = sql + f"WHERE s.id < {id} " 
        # If blank record then fetch the one with the highest id 
        sql = sql + " ORDER BY s.id DESC LIMIT 1 "        
        print(sql)

        record = db.executeSqlStatement(sql)[0]

        # If record retrieved set fields then return 
        if record:
            self.setFields(record)
        
        # NOTE: If not record retrieved None is returned 
        return record 

    def getFieldsAsDict(self):
        # TODO function description 
        fieldsDict = {
                'catalognumber':'"%s"' % self.catalogNumber , # TODO "{}".format(var...)
                'multispecimen':'"%s"' % self.multiSpecimen ,
                'taxonname':'"%s"' % self.taxonName ,
                'taxonnameid':'"%s"' % self.taxonNameid ,
                'typestatusname':'"%s"' % self.typeStatusName ,
                'typestatusid':'%s' % self.typeStatusId ,
                'georegionname':'"%s"' % self.geoRegionName ,
                'georegionid':'"%s"' % self.geoRegionId ,
                'storagefullname':'"%s"' % self.storageFullName,
                'storagename':'"%s"' % self.storageName ,
                'storageid':'"%s"' % self.storageId ,
                'preptypename':'"%s"' % self.prepTypeName ,
                'preptypeid':'"%s"' % self.prepTypeId ,
                'notes':'"%s"' % self.notes ,
                'institutionid':'"%s"' % self.institutionId ,
                'collectionid':'"%s"' % self.collectionId ,
                'username':'"%s"' % self.userName ,
                'userid':'"%s"' % self.userId ,
                'workstation':'"%s"' % self.workStation ,
                'recorddatetime':'"%s"' % self.recordDateTime ,
                'exported':'"%s"' % self.exported ,
                'exportdatetime':'"%s"' % self.exportDateTime ,
                'exportuserid':'"%s"' % self.exportUserId ,
                }
        print(len(fieldsDict))
        return fieldsDict
    
    def setStorageFields(self, index):
        self.storageId = self.storageLocations[index]['id']
        self.storageName = self.storageLocations[index]['name']
        self.storageFullName = self.storageLocations[index]['fullname']
    
    def setPrepTypeFields(self,index):
        self.prepTypeId = self.prepTypes[index]['id']
        self.prepTypeName = self.prepTypes[index]['name']

    def setTypeStatusFields(self,index):
        # Get type status record on the basis of list index 
        self.typeStatusId = self.typeStatuses[index]['id']
        self.typeStatusName = self.typeStatuses[index]['name']

    def setgeoRegionFields(self,index):
        self.geoRegionId = self.geoRegions[index]['id']
        self.geoRegionName = self.geoRegions[index]['name']
