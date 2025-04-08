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

import os
import sys
from datetime import datetime

# Internal dependencies
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Internal dependencies
import util
import global_settings as gs
from .model import Model
from models import collection as coll


class Specimen(Model):
    """
    The specimen class is a representation of a specimen record to hold its data
    Any instance is either an existing record in the database or transient pending an insert
    """

    def __init__(self, collection_id):
        """
        Set up blank specimen record instance for data entry on basis of collection id 
        """
        # self.fieldsasdict = Model.getFieldsAsDict()

        Model.__init__(self, collection_id)
        self.table = 'specimen'
        self.apiname = 'collectionobject'
        self.id = 0
        self.catalogNumber = ''
        self.taxonFullName = ''
        self.taxonName = ''
        self.taxonAuthor = ''
        self.taxonNameId = 0
        self.taxonSpid = 0
        self.taxonDasscoId = 0
        self.taxonRankName = ''  # TODO
        self.familyName = ''  # TODO
        self.higherTaxonName = ''
        self.taxonNumber = ''
        self.taxonNrSource = ''
        self.typeStatusName = ''
        self.typeStatusId = 0
        self.objectCondition = ''
        self.specimenObscured = False
        self.labelObscured = False
        self.geoRegionName = ''
        self.geoRegionSource = ''
        self.geoRegionId = 0
        self.storageFullName = ''
        self.storageName = ''
        self.storageId = 0
        self.storageRankName = ''
        self.prepTypeName = ''
        self.prepTypeId = 0
        self.notes = ''
        self.containername = ''
        self.containertype = ''
        self.institutionId = gs.institutionId  # self.db.getRowOnId('collection',collection_id)['institutionid']
        self.institutionName = gs.institutionName
        self.collectionId = collection_id
        self.collectionName = gs.collectionName
        self.collection = coll.Collection(collection_id)
        self.userName = gs.userName
        self.userId = gs.spUserId
        self.firstName = gs.firstName
        self.middleInitial = gs.middleInitial
        self.lastName = gs.lastName
        self.recordDateTime = str(datetime.now())
        self.exported = 0
        self.exportDateTime = ''
        self.exportUserId = ''

        # Predefined data fields
        self.storageLocations = None
        self.prepTypes = None
        self.typeStatuses = None
        self.geoRegions = None
        # self.geoRegionSources = None

        self.loadPredefinedData()

    def loadPredefinedData(self):
        """
        Function for loading predefined data in order to get primary keys and other info to be pooled from at selection in GUI.
        """

        self.storageLocations = self.db.getRowsOnFilters('storage', {'collectionid =': f'{self.collectionId}'})
        self.prepTypes = self.db.getRowsOnFilters('preptype', {'collectionid =': f'{self.collectionId}'}, 100, 'name')
        self.typeStatuses = self.db.getRowsOnFilters('typestatus', {'collectionid =': f'{self.collectionId}'}, 100, 'ordinal')
        self.geoRegions = self.db.getRowsOnFilters('georegion', {'collectionid =': f'{self.collectionId}'})
        # self.geoRegionSources = self.db.getRowsOnFilters('georegionsource', {'collectionid =': f'{self.collectionId}'})

    def getFieldsAsDict(self):
        """
        Generates a dictonary with database column names as keys and specimen records fields as values
        RETURNS said dictionary for passing on to data access handler
        """
        if self.containername: #Check if containername is None
            self.containername = self.containername.strip()
        fieldsDict = {
            'id': f'{self.id}',
            'catalognumber': f'{self.catalogNumber}',
            'taxonfullname': f'{self.taxonFullName}',
            'taxonname': f'{self.taxonName}',
            'taxonauthor':f'{self.taxonAuthor}',
            'taxonnameid': f'{self.taxonNameId}',
            'familyname': f'{self.familyName}',
            'taxonspid': f'{self.taxonSpid}',
            'taxondasscoid': f'{self.taxonDasscoId}',
            'highertaxonname': f'{self.higherTaxonName}',
            'rankid': f'{self.rankid}',
            'taxonrankname': f'{self.taxonRankName}',
            'taxonnumber': f'{self.taxonNumber}',
            'taxonnrsource': f'{self.taxonNrSource}',
            'typestatusname': f'{self.typeStatusName}',
            'typestatusid': f'{self.typeStatusId}',
            'georegionname': f'{self.geoRegionName}',
            'georegionsource': f'{self.geoRegionSource}',
            'georegionid': f'{self.geoRegionId}',
            'storagefullname': f'{self.storageFullName}',
            'storagename': f'{self.getStorageName()}',
            'storageid': f'{self.storageId}',
            'storagerankName': f'{self.storageRankName}',
            'preptypename': f'{self.prepTypeName}',
            'preptypeid': f'{self.prepTypeId}',
            'objectcondition': f'{self.objectCondition}',
            'specimenobscured':f'{self.specimenObscured}',
            'labelobscured':f'{self.labelObscured}',
            'notes': f'{self.notes}',
            'containername': f'{self.containername}',
            'containertype': f'{self.containertype}',
            'institutionid': f'{self.institutionId}',
            'institutionname': f'{self.institutionName}',
            'collectionid': f'{self.collectionId}',
            'collectionname': f'{self.collectionName}',
            'username': f'{self.userName}',
            'userid': f'{self.userId}',
            'agentfirstname': f'{self.firstName}',
            'agentmiddleinitial': f'{self.middleInitial}',
            'agentlastname': f'{self.lastName}',
            # 'workstation':     f'{self.workStation}',
            'recorddatetime': f'{self.recordDateTime}',
            'exported': f'{self.exported}',
            'exportdatetime': f'{self.exportDateTime}',
            'exportuserid': f'{self.exportUserId}'
        }

        return fieldsDict

    def setFields(self, record):
        """
        Function for setting specimen data field from record
        CONTRACT
           record: sqliterow object containing specimen record data
        """
        # model.Model.setFields(self, record)

        if record is not None:
            util.logger.debug(f'Initializing specimen record with keys: {record.keys()}')

            self.id = record['id']
            self.catalogNumber = record['catalognumber']
            self.containername = record['containername']
            self.containertype = record['containertype']
            self.taxonFullName = record['taxonfullname']
            self.taxonName = record['taxonname']
            self.taxonAuthor = record['taxonauthor']
            self.taxonNameId = record['taxonnameid']
            self.familyName = record['familyname']
            self.taxonSpid = record['taxonspid']
            self.taxonDasscoId = record['taxondasscoid']
            self.higherTaxonName = record['highertaxonname']
            self.rankid = record['rankid']
            self.taxonRankName = record['taxonrankname']
            self.taxonNumber = record['taxonnumber']
            self.taxonNrSource = record['taxonnrsource']
            self.typeStatusName = record['typestatusname']
            self.typeStatusId = record['typestatusid']
            self.objectCondition = record['objectcondition']
            self.specimenObscured = record['specimenobscured']
            self.labelObscured = record['labelobscured']
            self.geoRegionName = record['georegionname']
            self.geoRegionSource = record['georegionsource']
            self.geoRegionId = record['georegionid']
            self.storageFullName = record['storagefullname']
            self.storageName = record['storagename']
            self.storageId = record['storageid']
            self.storageRankName = record['storagerankname']
            self.prepTypeName = record['preptypename']
            self.prepTypeId = record['preptypeid']
            self.notes = record['notes']
            self.containername = record['containername']
            self.containertype = record['containertype']
            self.institutionId = record['institutionid']
            self.institutionName = record['institutionname']
            self.collectionId = record['collectionid']
            self.collectionName = record['collectionname']
            self.userName = record['username']
            self.userId = record['userid']
            self.firstName = record['agentfirstname']
            self.middleInitial = record['agentmiddleinitial']
            self.lastName = record['agentlastname']
            self.recordDateTime = record['recorddatetime']
            self.exported = record['exported']
            self.exportDateTime = record['exportdatetime']
            self.exportUserId = record['exportuserid']
            # self.agentfullname = record['agentfullname']
        else:
            pass

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
        Listboxes and combos in PySimpleGui can't hold key/value pairs, so the index was needed to find the corresponding record.
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

    def setPrepTypeFields(self, index):
        """
        Get prep type record on the basis of list index
            and set respective fields
        """
        if index >= 0:  # Apparently, index -1 selects the last item in the list
            self.prepTypeId = self.prepTypes[index]['id']
            self.prepTypeName = self.prepTypes[index]['name']

    def setTypeStatusFields(self, index):
        """
        Get type status record on the basis of list index
            and set respective fields
        """
        if index >= 0:  # Apparently, index -1 selects the last item in the list
            self.typeStatusId = self.typeStatuses[index]['id']
            self.typeStatusName = self.typeStatuses[index]['name']

    def setGeoRegionFields(self, index):
        """
        Get type status record on the basis of list index
            and set respective fields
        """
        if index >= 0:  # Apparently, index -1 selects the last item in the list
            self.geoRegionId = self.geoRegions[index]['id']
            self.geoRegionName = self.geoRegions[index]['name']
            self.geoRegionSource = self.geoRegions[index]['source']

    def setStorageFields(self, index):
        """
        Get storage record on the basis of list index
            and set respective fields
        """
        self.storageId = self.storageLocations[index]['id']
        self.storageName = self.storageLocations[index]['name']
        self.storageFullName = self.storageLocations[index]['fullname']
        self.storageRankName = self.storageLocations[index]['storagerankname']

    def setStorageFieldsFromRecord(self, storageRecord):
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
            self.storageRankName = storageRecord['rankname']
        else:
            # Empty record

            self.storageId = 0

        return self.storageId

    def setStorageFieldsFromModel(self, object):
        """
        Get storage record on the basis of list index
            and set respective fields
        """
        self.storageId = object.id
        self.storageName = object.name
        self.storageFullName = object.fullName
        self.storageRankName = object.rankName

    def setTaxonNameFields(self, record):
        """
        Set taxon name fields from selected name record
        CONTRACT
          record (sqliterow) : SQLite Row holding taxon name record
        RETURNS taxonNameId (int) :
        """
        if record is not None:
            self.taxonNameId = record['id']
            self.taxonSpid = record['spid']
            self.taxonDasscoId = record['dasscoid']
            self.taxonName = record['name']
            self.taxonAuthor = record['author']
            self.taxonFullName = record['fullname']
            self.higherTaxonName = record['parentfullname']
            self.rankid = record['rankid']  # TODO
            self.taxonNumber = record['idnumber']
            self.taxonNrSource = record['taxonnrsource']
            self.taxonRankName = self.getTaxonRankname(self.rankid)
            self.familyName = self.searchParentTaxon(self.taxonFullName, 140, self.collection.taxonTreeDefId)
            pass
            # self.notes = f"{self.notes} | {record['notes']}"
        else:
            # Empty record
            self.taxonNameId = 0
            self.taxonSpid = 0
            self.taxonDasscoId = ''
            self.taxonName = ''
            self.taxonAuthor = ''
            self.taxonFullName = ''
            self.higherTaxonName = ''
            self.rankid = ''
            self.taxonNumber = ''
            self.taxonNrSource = ''
            self.taxonRankName = ''
            self.familyName = ''

        return self.taxonNameId

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
            self.storageFullName = storageRecord[0]['storagerankname']
        elif resultsRowCount == 0:
            # Unknown storage full name, add verbatim
            self.storageFullName = storageFullName
            self.storageId = 0
        else:
            # Duplicate fullnames detected
            self.storageId = -1

        return self.storageId

    def setTaxonNameFieldsFromRecord(self, record):
        """
        Set taxon name fields from selected name record
        CONTRACT
          record (sqliterow) : SQLite Row holding taxon name record
        RETURNS taxonNameId (int) :
        """

        if record is not None:
            self.taxonNameId = record['id']
            self.taxonSpid = record['spid']
            self.taxonDasscoId = record['dasscoid']
            self.taxonName = record['name']
            self.taxonAuthor = record['author']
            self.taxonFullName = record['fullName']
            self.rankid = record['rankid']  # TODO: taxonrankid
            self.taxonRankName = self.getTaxonRankname(record['rankid'])
            self.higherTaxonName = record['parentFullName']
            self.familyName = self.searchParentTaxon(self.taxonFullName, 140, self.collection.taxonTreeDefId)
            self.taxonNumber = record['idnumber']            
            self.taxonNrSource = record['taxonnrsource']

        else:
            # Empty record
            self.taxonNameId = 0
        return self.taxonNameId

    def setTaxonNameFieldsFromModel(self, object):
        """
        Set taxon name fields from selected taxon name mode instance
        CONTRACT
          object (Model) : Taxon name model object instance 
        RETURNS taxonNameId (int) :
        """

        if object is not None:
            self.taxonNameId = object.id
            self.taxonSpid = object.spid
            self.taxonDasscoId = object.dasscoid
            self.taxonName = object.name
            self.taxonAuthor = object.author
            self.taxonFullName = object.fullName
            self.rankid = object.rankid  # TODO: taxonrankid
            self.taxonRankName = self.getTaxonRankname(object.rankid)
            self.higherTaxonName = object.parentFullName
            self.familyName = self.searchParentTaxon(self.taxonFullName, 140, self.collection.taxonTreeDefId)
            self.taxonNumber = object.idNumber
            self.taxonNrSource = object.idSource

        else:
            # Empty record
            self.taxonNameId = 0
        return self.taxonNameId

    def getTaxonRankname(self, rankid):
        """ Return Taxon Rank name as based on rank id """

        taxonRank = 'unknown'

        taxonRanks = {
            0: 'Life',
            10: 'Kingdom',
            20: 'Subkingdom',
            30: 'Phylum',
            40: 'Subphylum',
            50: 'Superclass',
            60: 'Class',
            70: 'Subclass',
            80: 'Infraclass',
            90: 'Superorder',
            100: 'Order',
            110: 'Suborder',
            120: 'Infraorder',
            130: 'Superfamily',
            140: 'Family',
            150: 'Subfamily',
            160: 'Tribe',
            170: 'Subtribe',
            180: 'Genus',
            190: 'Subgenus',
            220: 'Species',
            230: 'Subspecies',
            240: 'variety',
            250: 'subvariety',
            260: 'forma',
            270: 'subforma'
        }

        if rankid in taxonRanks:
            taxonRank = taxonRanks[rankid]

        return taxonRank

    def setTaxonNameFieldsUsingFullName(self, taxonFullName):
        """
        Get taxon name record on the basis of full name and set respective fields
        CONTRACT
          taxonFullName (string) : Fullname value of selected taxon
        RETURNS taxonNameId (int) : Primary key of selected taxon record
        """
        
        # Replace apostrophes with double quotes for SQL query
        taxonFullName = taxonFullName.replace("'", "''")

        # Get taxon name record on fullname
        taxonNameRecord = self.db.getRowsOnFilters('taxonname', {'fullname =': f'"{taxonFullName}"'})
        resultsRowCount = len(taxonNameRecord)

        # if result not empty (or > 1) then set fields
        if resultsRowCount == 1:
            self.taxonNameId = taxonNameRecord[0]['id']
            self.taxonName = taxonNameRecord[0]['name']
            self.taxonAuthor = taxonNameRecord[0]['author']
            self.taxonFullName = taxonNameRecord[0]['fullname']
            self.higherTaxonName = taxonNameRecord[0]['highertaxonname']
            self.taxonSpid = taxonNameRecord[0]['spid']
            self.taxonDasscoId = taxonNameRecord[0]['dasscoid']
        elif resultsRowCount == 0:
            # Unknown taxon name, add verbatim
            self.taxonFullName = taxonFullName
            self.taxonNameId = 0
        else:
            # Duplicate fullnames detected
            self.taxonNameId = -1

        return self.taxonNameId

    def getStorageName(self):
        """
        Method for ensuring that 'None' values generated by the UI are saved as blanks
        """
        if self.storageName == 'None':
            return ''
        else:
            return self.storageName

    def determineRank(self, taxonNameEntry):
        """
        Determine rank of given taxon name entry by analysing string pattern. 
        Typical patterns: 
            Genus species 
            Genus species subspecies 
            Genus species var. variety 
            Genus species f. forma 
            Genus species x species 
            Genus (Subgenus) species 
            Genus (Subgenus) species subspecies 
            etcetera 
        CONTRACT
          taxonNameEntry (string) : Full taxon name entry to be analysed
        RETURNS rankid (int)      : Rank id number 
        """
        rankid = 999 # default rank id value corresponding to no rank at all in case the analysis fails. 
        try:
            # In case an author name is included in the full taxon name, this should be separated out by an underscore
            #authorName = '' # Initialize author name string as blank 
            #authorSplit = taxonNameEntry.split('_') # Split out author name part of entry, if it exists 

            # If an underscore is detected, the second element of the split is assumed to be the author name
            #if len(authorSplit) > 1: authorName = authorSplit[1]
            #taxonName = authorSplit[0] # The first or only element is assumed to be the taxon name 

            # Split taxon name in respective elements and get element count 
            taxonNameSplit = taxonNameEntry.strip().split(' ')
            elementCount = len(taxonNameSplit)

            # Check for subgenus; If present, the subgenus is the second element enclosed by parentheses 
            subgenusCount = 0
            if taxonNameSplit[1][1] == '(': 
                subgenusCount = 1 # The subgenus adds another element to the total count 

            # Look for distinctive string patterns indicating rank 
            if ' var. ' in taxonNameEntry:
                rankid = 240 # Variety 
            elif ' subvar.  ' in taxonNameEntry:
                rankid = 250 # Subvariety 
            elif ' f. ' in taxonNameEntry:
                rankid = 260 # Forma 
            elif ' subf. ' in taxonNameEntry:
                rankid = 270 # Subforma
            elif ' x ' in taxonNameEntry:
                rankid = 220 # Hybrids are always of rank species 
            # Otherwise look for element count indicating rank:
            elif elementCount == 3 + subgenusCount:
                rankid = 230 # Subspecies 
            elif elementCount == 2 + subgenusCount:
                rankid = 220 # Species 
            elif elementCount == 1 + subgenusCount:
                rankid = 180 # Genus 
        except:
            util.logger.error(f'Could not determine rank of novel taxon: {taxonNameEntry}')

        return rankid

    def searchParentTaxon(self, taxonFullName, target_rankid, treedefid):
        """
        Will recursively traverse a given taxon's parental lineage until it hits the target rank
        CONTRACT
            taxonFullName (string) : The taxon name to acquire the parent taxon name for
            target_rankid: Target rank id of the parent taxon to be searched for
        RETURNS taxonFullName (string) : Name of the parent taxon 
        """
        
        # Replace apostrophes with double quotes for SQL query
        taxonFullName = taxonFullName.replace("'", "''")

        taxonRankId = 270  # Start with lowest possible rank

        # Keep on traversing parental branch until the specified rank level has been passed
        while (taxonRankId >= target_rankid):
            # Get current taxon record on fullname and taxon tree
            taxonNameRecords = self.db.getRowsOnFilters('taxonname', filters={'fullname': f"='{taxonFullName}'",'treedefid': f"= '{treedefid}'"})

            if len(taxonNameRecords) > 0:
                # First check whether this is an accepted name or synonym; If the latter, use the accepted name instead as basis record
                acceptedFullName = taxonNameRecords[0]['acceptedfullname'].replace("'", "''")
                if acceptedFullName != '' and acceptedFullName is not None:
                    taxonNameRecords = self.db.getRowsOnFilters('taxonname', filters={'fullname': f"='{acceptedFullName}'",'treedefid': f"= '{treedefid}'"})

                if len(taxonNameRecords) > 0:
                    taxonRankId = taxonNameRecords[0]['rankid']
                    taxonFullName = taxonNameRecords[0]['fullname']
                    parentName = taxonNameRecords[0]['parentfullname']  # TODO More secure with primary keys
                else: 
                    # Could not retrieved accepted taxonname: Abort 
                    taxonFullName = ''
                    break

                # Return when given taxon already matches rank or is of higher rank
                if taxonRankId <= target_rankid:
                    if taxonRankId < target_rankid: taxonFullName = ''  # Clear taxon name if higher than target rank
                    break 
                else:
                    # Target rank not yet hit; check next parent in line
                    return (self.searchParentTaxon(parentName, target_rankid, treedefid)) 

            else:
                # Can't find (further) parent taxon
                taxonFullName = '-parent not found-'
                # raise Exception(f"Could not retrieve parent taxon of target rank: {target_rankid} !")
                break  # return current

        return taxonFullName

    def __str__(self):
        return f'[{self.table}] id:{self.id}, name:{self.name}, fullname = {self.fullName}, notes = {self.notes}'
