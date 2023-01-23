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
import data_access
import global_settings as gs

class specimen(model.Model):
    """
    The specimen class is a representation of a specimen record to hold its data
    Any instance is either an existing record in the database or transient pending an insert
    """

    def __init__(self, collection_id):
        """
        Set up blank specimen record instance for data entry on basis of collection id 
        """ 
        model.Model.__init__(self, collection_id)
        self.table           = 'specimen'   
        self.apiname         = 'collectionobject'
        self.id              = 0
        self.catalogNumber   = ''
        self.multiSpecimen   = 'False'
        self.taxonFullName   = ''
        self.taxonName       = ''
        self.taxonNameId     = 0
        #self.taxonspid 
        self.higherTaxonName = ''
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
        self.institutionId   = gs.institutionId #self.db.getRowOnId('collection',collection_id)['institutionid']
        self.institutionName = gs.institutionName
        self.collectionId    = collection_id
        self.collectionName  = gs.collectionName
        self.userName        = gs.spUserName
        self.userId          = gs.spUserId
        # self.workStation     = ''
        self.recordDateTime  = str(datetime.now())
        self.exported        = 0
        self.exportDateTime  = ''
        self.exportUserId    = ''

        # Predefined data fields
        self.storageLocations = None 
        self.prepTypes = None 
        self.typeStatuses = None 
        self.geoRegions = None 
        #self.geoRegionSources = None 

        self.loadPredefinedData()

# Overriding inherited functions

    def loadPredefinedData(self):
        """
        Function for loading predefined data in order to get primary keys and other info to be pooled from at selection in GUI.
        """
        
        self.storageLocations = self.db.getRowsOnFilters('storage', {'collectionid =': f'{self.collectionId}'})
        self.prepTypes = self.db.getRowsOnFilters('preptype', {'collectionid =': f'{self.collectionId}'}, 100, 'name')
        self.typeStatuses = self.db.getRowsOnFilters('typestatus', {'collectionid =': f'{self.collectionId}'}, 100, 'name')
        self.geoRegions = self.db.getRowsOnFilters('georegion', {'collectionid =': f'{self.collectionId}'}) 
        #self.geoRegionSources = self.db.getRowsOnFilters('georegionsource', {'collectionid =': f'{self.collectionId}'}) 

    def getFieldsAsDict(self):
        """
        Generates a dictonary with database column names as keys and specimen records fields as values 
        RETURNS said dictionary for passing on to data access handler 
        """
        
        fieldsDict = {
                'catalognumber':   f'"{self.catalogNumber}"', 
                'multispecimen':   f'"{self.multiSpecimen}"',
                'taxonfullname':   f'"{self.taxonFullName}"', 
                'taxonname':       f'"{self.taxonName}"',
                'taxonnameid':     f'"{self.taxonNameId}"',
                'typestatusname':  f'"{self.typeStatusName}"',
                'typestatusid':    f'"{self.typeStatusId}"',
                'highertaxonname': f'"{self.higherTaxonName}"',
                'georegionname':   f'"{self.geoRegionName}"',
                'georegionid':     f'"{self.geoRegionId}"',
                'storagefullname': f'"{self.storageFullName}"',
                'storagename':     f'"{self.storageName}"',
                'storageid':       f'"{self.storageId}"',
                'preptypename':    f'"{self.prepTypeName}"',
                'preptypeid':      f'"{self.prepTypeId}"',
                'notes':           f'"{self.notes}"',
                'institutionid':   f'"{self.institutionId}"',
                'institutionname':  f'"{self.institutionName}"',
                'collectionid':    f'"{self.collectionId}"',
                'collectionname':  f'"{self.collectionName}"',
                'username':        f'"{self.userName}"',
                'userid':          f'"{self.userId}"',
                # 'workstation':     f'"{self.workStation}"',
                'recorddatetime':  f'"{self.recordDateTime}"',
                'exported':        f'"{self.exported}"',
                'exportdatetime':  f'"{self.exportDateTime}"',
                'exportuserid':    f'"{self.exportUserId}"',
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
        self.catalogNumber = record['catalognumber']
        self.multiSpecimen = record['multispecimen']
        self.taxonFullName = record['taxonfullname']
        self.taxonName = record['taxonname']
        self.taxonNameId = record['taxonnameid']
        #self.taxonspid = record['taxonspid']
        self.higherTaxonName = record['highertaxonname']
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
        self.institutionName = record['institutionname']
        self.collectionId = record['collectionid']
        self.collectionName = record['collectionname']
        self.userName = record['username']
        self.userId = record['userid']

        self.recordDateTime = record['recorddatetime']
        self.exported = record['exported']
        self.exportDateTime = record['exportdatetime']
        self.exportUserId = record['exportuserid']

        self.loadPredefinedData()
    
# Specimen class specific functions 

    def setStickyFields(self, record):
        """
        Set all sticky fields for a given record 
        """

        self.setStorageFields(record)
        self.setPrepTypeFields(record)
        self.setTaxonNameFields(record)

    def setListFields(self, fieldName, index):
        """
        Generic function for setting the respective list fields. 
        Listboxes and combos in PySimpleGui can't hold key/value pairs, so the index is needed to find the corresponding record. 
        CONTRACT
            fieldName (String) : Name of the input field to be set 
            index (Integer)    : Index of the 
        """
        if fieldName == 'cbxPrepType':
            self.setPrepTypeFields(index)
        elif fieldName == 'cbxTypeStatus':
            self.setTypeStatusFields(index)
        elif fieldName == 'cbxGeoRegion':
            self.setgeoRegionFields(index) 
    
    def setPrepTypeFields(self,index):
        """
        Get prep type record on the basis of list index 
            and set respective fields 
        """
        self.prepTypeId = self.prepTypes[index]['id']
        self.prepTypeName = self.prepTypes[index]['name']

    def setTypeStatusFields(self,index):
        """
        Get type status record on the basis of list index 
            and set respective fields 
        """
        self.typeStatusId = self.typeStatuses[index]['id']
        self.typeStatusName = self.typeStatuses[index]['name']

    def setGeoRegionFields(self,index):
        """
        Get type status record on the basis of list index 
            and set respective fields 
        """
        self.geoRegionId = self.geoRegions[index]['id']
        self.geoRegionName = self.geoRegions[index]['name']       

    def setStorageFields(self, index):
        """
        Get storage record on the basis of list index 
            and set respective fields
        """
        self.storageId = self.storageLocations[index]['id']
        self.storageName = self.storageLocations[index]['name']
        self.storageFullName = self.storageLocations[index]['fullname']     

    def setStorageFieldsFromModel(self, object):
        """
        Get storage record on the basis of list index 
            and set respective fields
        """
        self.storageId = object.id
        self.storageName = object.name
        self.storageFullName = object.fullName
    
    def setTaxonNameFields(self, taxonNameRecord):
        """
        Set taxon name fields from selected name record
        CONTRACT
          taxonNameRecord (sqliterow) : SQLite Row holding taxon name record
        RETURNS taxonNameId (int) : 
        """
        if taxonNameRecord is not None: 
            self.taxonNameId = taxonNameRecord['id'] 
            self.taxonName = taxonNameRecord['name'] 
            self.taxonFullName = taxonNameRecord['fullname'] 
            self.higherTaxonName = taxonNameRecord['parentfullname'] 
        else:
            # Empty record 
            self.taxonNameId = 0

        return self.taxonNameId
    
    def setTaxonNameFieldsFromModel(self, object):
        """
        Set taxon name fields from selected name record
        CONTRACT
          taxonNameRecord (sqliterow) : SQLite Row holding taxon name record
        RETURNS taxonNameId (int) : 
        """
        if object is not None: 
            self.taxonNameId = object.id
            self.taxonName = object.name
            self.taxonFullName = object.fullName
            self.higherTaxonName = object.parentFullName
        else:
            # Empty record 
            self.taxonNameId = 0

        return self.taxonNameId
    
    def setTaxonNameFieldsUsingFullName(self, taxonFullName):
        """
        Get taxon name record on the basis of full name  
           and set respective fields 
        CONTRACT 
          taxonFullName (string) : Fullname value of selected taxon 
        RETURNS taxonNameId (int) : Primary key of selected taxon record 
        """
        # Get taxon name record on fullname
        taxonNameRecord = self.db.getRowsOnFilters('taxonname', {'fullname =': f'"{taxonFullName}"'})
        resultsRowCount = len(taxonNameRecord)

        # if result not empty (or > 1) then set fields
        if resultsRowCount == 1:
            self.taxonNameId = taxonNameRecord[0]['id'] 
            self.taxonName = taxonNameRecord[0]['name'] 
            self.taxonFullName = taxonNameRecord[0]['fullname'] 
            self.higherTaxonName = taxonNameRecord[0]['highertaxonname'] 
        elif resultsRowCount == 0:
            # Unknown taxon name, add verbatim 
            self.taxonFullName = taxonFullName 
            self.taxonNameId = 0
        else:
            # Duplicate fullnames detected
            self.taxonNameId = -1

        return self.taxonNameId 

    def setStorageFields(self, storageRecord):
        """
        Set storage fields from selected storage location record
            CONTRACT
                storageRecord (sqliterow) : SQLite Row holding storage location record
            RETURNS taxonNameId (int) : Primary key of taxon name record 
        """

        if storageRecord is not None: 
            self.storageId = storageRecord['id'] 
            self.storageName = storageRecord['name']
            self.storageFullName = storageRecord['fullname'] 
        else:
            # Empty record 
            self.storageId = 0

        return self.storageId

    def setStorageFieldsUsingFullName(self, storageFullName):
        """
        Get storage record on the basis of full name and set respective fields 
        CONTRACT 
            storageFullName (string) : Fullname value of selected storage location 
            RETURNS storageId (int) : Primary key of selected storage location record
        """ 
        
        # Get storage record on fullname
        storageRecord = self.db.getRowsOnFilters('storage', {'fullname =': f'"{storageFullName}"'})
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
