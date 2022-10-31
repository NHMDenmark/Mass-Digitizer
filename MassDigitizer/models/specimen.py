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
from models import model
import data_access as db
import global_settings as gs

class specimen(model.Model):
    # The specimen class is a representation of a specimen record to hold its data
    # Any instance is either an existing record in the database or transient pending an insert

    def __init__(self, collection_id):
        """
        Set up blank specimen record instance for data entry on basis of collection id 
        """ 
        self.table           = 'specimen'   
        self.apiname         = 'collectionobject'
        self.id              = 0
        self.catalogNumber   = ''
        self.multiSpecimen   = 'False'
        self.taxonFullName   = ''
        self.taxonName       = ''
        self.taxonNameId     = 0
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
    
    def setFields(self, record):
        """
        Function for setting base object data field from record 
        CONTRACT 
           record: sqliterow object containing record data 
        """
        
        self.id = record['id']
        self.catalogNumber = record['catalognumber']
        self.multiSpecimen = record['multispecimen']
        self.taxonName = record['taxonname']
        self.taxonNameId = record['taxonnameid']
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

    def getFieldsAsDict(self):
        # Generates a dictonary with database column names as keys and specimen records fields as values 
        # RETURNS said dictionary for passing on to data access handler 
        fieldsDict = {
                'catalognumber':'"%s"' % self.catalogNumber , # TODO "{}".format(var...)
                'multispecimen':'"%s"' % self.multiSpecimen ,
                'taxonfullname':'"%s"' % self.taxonFullName ,
                'taxonname':'"%s"' % self.taxonName ,
                'taxonnameid':'"%s"' % self.taxonNameId ,
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
        
        return fieldsDict
    
    def setStickyFields(self, record):
        # TODO uncertain about this one  

        self.setStorageFields(record)
        self.setPrepTypeFields(record) # TODO 
        self.setTaxonNameFields(record)
        
    def setListFields(self, fieldName, index):
        # Generic function for setting the respective list fields 
        if fieldName == 'cbxPrepType':
            self.setPrepTypeFields(index)
        elif fieldName == 'cbxTypeStatus':
            self.setTypeStatusFields(index)
        elif fieldName == 'cbxGeoRegion':
            self.setgeoRegionFields(index) 
    
    def setPrepTypeFields(self,index):
        # Get prep type record on the basis of list index 
        #    and set respective fields 
        self.prepTypeId = self.prepTypes[index]['id']
        self.prepTypeName = self.prepTypes[index]['name']

    def setTypeStatusFields(self,index):
        # Get type status record on the basis of list index 
        #    and set respective fields 
        self.typeStatusId = self.typeStatuses[index]['id']
        self.typeStatusName = self.typeStatuses[index]['name']

    def setGeoRegionFields(self,index):
        # Get type status record on the basis of list index 
        #    and set respective fields 
        self.geoRegionId = self.geoRegions[index]['id']
        self.geoRegionName = self.geoRegions[index]['name']       

    def setStorageFields(self, index):
        # Get storage record on the basis of list index 
        # and set respective fields
        self.storageId = self.storageLocations[index]['id']
        self.storageName = self.storageLocations[index]['name']
        self.storageFullName = self.storageLocations[index]['fullname']
    
    def setTaxonNameFields(self, taxonNameRecord):
        # Set taxon name fields from selected name record
        # CONTRACT
        #   taxonNameRecord (sqliterow) : SQLite Row holding taxon name record
        # RETURNS taxonNameId (int) : 
        
        if taxonNameRecord is not None: 
            self.taxonNameId = taxonNameRecord['id'] 
            self.taxonName = taxonNameRecord['name'] 
            self.taxonFullName = taxonNameRecord['fullname'] 
        else:
            # Empty record 
            self.taxonNameId = 0

        return self.taxonNameId
    
    def setTaxonNameFieldsUsingFullName(self, taxonFullName):
        # Get taxon name record on the basis of full name  
        #    and set respective fields 
        # CONTRACT 
        #   taxonFullName (string) : Fullname value of selected taxon 
        # RETURNS taxonNameId (int) : Primary key of selected taxon record 
        
        # Get taxon name record on fullname
        taxonNameRecord = db.getRowsOnFilters('taxonname', {'fullname =': f'"{taxonFullName}"'})
        resultsRowCount = len(taxonNameRecord)

        # if result not empty (or > 1) then set fields
        if resultsRowCount == 1:
            self.taxonNameId = taxonNameRecord[0]['id'] 
            self.taxonName = taxonNameRecord[0]['name'] 
            self.taxonFullName = taxonNameRecord[0]['fullname'] 
        elif resultsRowCount == 0:
            # Unknown taxon name, add verbatim 
            self.taxonFullName = taxonFullName 
            self.taxonNameId = 0
        else:
            # Duplicate fullnames detected
            self.taxonNameId = -1

        return self.taxonNameId 

    def setStorageFields(self, storageRecord):
        # Set storage fields from selected storage location record
        # CONTRACT
        #   storageRecord (sqliterow) : SQLite Row holding storage location record
        # RETURNS taxonNameId (int) : 
        
        if storageRecord is not None: 
            self.storageId = storageRecord['id'] 
            self.storageName = storageRecord['name'] 
            self.storageFullName = storageRecord['fullname'] 
        else:
            # Empty record 
            self.storageId = 0

        return self.storageId

    def setStorageFieldsUsingFullName(self, storageFullName):
        # Get storage record on the basis of full name  
        #    and set respective fields 
        # CONTRACT 
        #   storageFullName (string) : Fullname value of selected storage location 
        # RETURNS storageId (int) : Primary key of selected storage location record 
        
        # Get storage record on fullname
        storageRecord = db.getRowsOnFilters('storage', {'fullname =': f'"{storageFullName}"'})
        resultsRowCount = len(storageFullName)

        # if result not empty (or > 1) then set fields
        if resultsRowCount == 1:
            self.storageId = storageRecord[0]['id'] 
            self.storageName = storageRecord[0]['name'] 
            self.storageFullName = storageRecord[0]['fullname'] 
        elif resultsRowCount == 0:
            # Unknown storage full name, add verbatim 
            self.storageFullName = storageFullName 
            self.storageId = 0
        else:
            # Duplicate fullnames detected
            self.storageId = -1

        return self.storageId 
        
    def loadPredefinedData(self):
        # Function for loading predefined data in order to get primary keys and other info to be pooled at selection in GUI 
        self.storageLocations = db.getRowsOnFilters('storage', {'collectionid =': f'{self.collectionId}'})
        self.prepTypes = db.getRowsOnFilters('preptype', {'collectionid =': f'{self.collectionId}'})
        self.typeStatuses = db.getRowsOnFilters('typestatus', {'collectionid =': f'{self.collectionId}'})
        self.geoRegions = db.getRowsOnFilters('georegion', {'collectionid =': f'{self.collectionId}'}) 
        self.geoRegionSources = db.getRowsOnFilters('georegionsource', {'collectionid =': f'{self.collectionId}'}) 
