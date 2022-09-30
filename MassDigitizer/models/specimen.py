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

  PURPOSE: TODO 
"""
from attr import fields_dict
import pytz
from datetime import datetime

# Internal dependencies
import data_access as db
import sqlite3
import util

class specimen:
    # TODO description

    # id              = 0
    # catalogNumber   = ''
    # multiSpecimen   = 'False'
    # taxonName       = ''
    # taxonNameid     = 0
    # #taxonspid 
    # typeStatusName  = ''
    # typeStatusId    = 0
    # geoRegionName   = ''
    # geoRegionId     = 0
    # storageFullName = ''
    # storageName     = ''
    # storageId       = 0
    # prepTypeName    = ''
    # prepTypeId      = 0
    # notes           = ''
    # institutionId   = 0
    # collectionId    = 0
    # userName        = ''
    # userId          = 0
    # workStation     = ''
    # recordDateTime  = str(datetime.now())
    # exported        = 0
    # exportDateTime  = ''
    # exportUserId    = ''

    # # Predefined data
    # storageLocations = {}
    # prepTypes = {}
    # typeStatuses = {}
    # geoRegions = {} 
    # geoRegionSources = {}

    # # Navigation 
    # previousId = 0
    # nextId = 0

    def __init__(self, collectionId):
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
        self.institutionId   = 0
        self.collectionId    = 0
        self.userName        = ''
        self.userId          = 0
        self.workStation     = ''
        self.recordDateTime  = str(datetime.now())
        self.exported        = 0
        self.exportDateTime  = ''
        self.exportUserId    = ''
        
        # Predefined data
        self.storageLocations = db.getRowsOnFilters('storage', {'collectionid =': '%s'%collectionId})
        self.prepTypes = db.getRowsOnFilters('preptype', {'collectionid =': '%s'%collectionId})
        self.typeStatuses = db.getRowsOnFilters('typestatus', {'collectionid =': '%s'%collectionId})
        self.geoRegions = db.getRowsOnFilters('georegion', {'collectionid =': '%s'%collectionId}) 
        self.geoRegionSources = db.getRowsOnFilters('georegionsource', {'collectionid =': '%s'%collectionId}) 
        
        # Navigation 
        self.previousId = 0
        self.nextId = 0
    
    def save(self):
        # TODO Function description & contract     
        # fields must be a dictionary with the specimen table headers as 'keys' and the form field content as 'values'.
        # insert is a switch to mark whether an INSERT or an UPDATE is called for.
        # recordID is required for updates.
        #   RETURNS record id (primary key)
        if self.id > 0:
            print('Update specimen record with id: ', self.id)
            record = db.updateRow('specimen', self.id, self.getFieldsAsDict())
        else:
            # Checking if Save is a novel record , or if it is updating existing record.
            print('Insert new specimen record.')
            record = db.insertRow('specimen', self.getFieldsAsDict())
            self.id = record['id']

        return self.id

    def load(self, id):
        # TODO function description 
        record = db.getRowOnId(id)
        self.setFields(record)

    def setFields(self, record):
        # TODO function description 
        self.id = record['id']
        self.catalogNumber = record['catalogNumber'] 
        self.multiSpecimen = record['multiSpecimen'] 
        self.taxonName = record['taxonName'] 
        self.taxonNameid = record['taxonNameid'] 
        #self.taxonspid = record['taxonspid']
        self.typeStatusName = record['typeStatusName'] 
        self.typeStatusId = record['typeStatusId'] 
        self.geoRegionName = record['geoRegionName'] 
        self.geoRegionId = record['geoRegionId'] 
        self.storageFullName = record['storageFullName']
        self.storageName = record['storageName'] 
        self.storageId = record['storageId'] 
        self.prepTypeName = record['prepTypeName'] 
        self.prepTypeId = record['prepTypeId'] 
        self.notes = record['notes'] 
        self.institutionId = record['institutionId'] 
        self.collectionId = record['collectionId'] 
        self.userName = record['userName'] 
        self.userId = record['userId'] 
        self.workStation = record['workStation'] 
        self.recordDateTime = record['recorddateTime']
        self.exported = record['exported']
        self.exportDateTime = record['exportDateTime']
        self.exportUserId = record['exportUserId']

        # TODO navigation?
        #self.previousId = ? 
        #self.nextId = ?         

        # TODO predefinedData ? 

    def getFieldsAsDict(self):
        # TODO function description 
        fieldsDict = {
                'catalogNumber':'"%s"' % self.catalogNumber , # TODO "{}".format(var...)
                'multiSpecimen':'"%s"' % self.multiSpecimen ,
                'taxonName':'"%s"' % self.taxonName ,
                'taxonNameid':'"%s"' % self.taxonNameid ,
                'typeStatusName':'"%s"' % self.typeStatusName ,
                'typeStatusId':'%s' % self.typeStatusId ,
                'geoRegionName':'"%s"' % self.geoRegionName ,
                'geoRegionId':'"%s"' % self.geoRegionId ,
                'storageFullName':'"%s"' % self.storageFullName,
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
        self.storagename = self.storageLocations[index]['name']
        self.storageFullname = self.storageLocations[index]['fullname']
    
    def setPrepTypeFields(self,index):
        self.preptypeid = self.prepTypes[index]['id']
        self.preptypename = self.prepTypes[index]['name']

    def setTypeStatusFields(self,index):
        self.typestatusid = self.typeStatuses[index]['id']
        self.typestatusname = self.typeStatuses[index]['name']

    def setgeoRegionFields(self,index):
        self.geoRegionId = self.geoRegions[index]['id']
        self.geoRegionName = self.geoRegions[index]['name']

    def obtainTrack(self, incrementor=0):
        # TODO function contract
        # Keeps track of record IDs in relation to the Go-back button functionality.
        recordID = self.getRecordIDbyBacktracking(incrementor)
        if recordID:
            print(f'IN ID of obtainTrack() ;; {recordID}')
            # recordID = self.getRecordIDbyBacktracking(incrementor)
            return recordID
        else:
            print(f'In ELSE obtainTrack() -- {recordID}')
            # recordID = recordID - 1
            return recordID

    def getRecordIDbyBacktracking(self, backtrackCounter):
        # TODO function contract
        # TODO must be reworked to use SQL statements rather than "counters" which rely on sequential IDs!
        sql = "select * from specimen s order by s.id DESC LIMIT {},1;".format(backtrackCounter)
        print(sql)
        try:
            rows = db.executeSqlStatement(sql)
        except sqlite3.OperationalError:
            #window['txtTaxonName'].update("Beginning of taxon names reached.")
            print("Beginning of taxon names reached.")

        if rows:
            print('COUNTER row::::', rows[0])
            recordIDcurrent = rows[0]['id']
            return recordIDcurrent
        else:
            print('IN else clause due to no more GO_BACK !!')
            #window['btnBack'].update(disabled=True)
            #window['lblWarning'].update(visible=True)

            # backtrackCounter = backtrackCounter - 1
            return False
            # sql = "select * from specimen s  order by s.id DESC LIMIT {},1;".format(backtrackCounter)
            # rows = db.executeSqlStatement(sql)

        sql = "select * from specimen s  order by s.id DESC LIMIT {},1;".format(backtrackCounter)

        rows = db.executeSqlStatement(sql)
        if len(rows) > 0:
            print('COUNTER row::::', rows[0])
            recordIDcurrent = rows[0]['id']
        else:
            recordIDcurrent = 0

        return recordIDcurrent