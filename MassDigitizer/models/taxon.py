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

# Internal dependencies
from models import model
import data_access
import global_settings as gs

db = data_access.DataAccess(gs.databaseName)

class Taxon(model.Model):
    """
    The taxon class is a representation of a taxon record to hold its data
    Any instance is either an existing record in the database or transient pending an insert
    """

    def __init__(self, collection_id):
        """Set up blank taxon"""         
        model.Model.__init__(self, collection_id)
        self.table          = 'taxon'
        self.sptype         = 'taxon'
        self.author         = ''
        self.rankId         = 0
        self.duplicateSpid  = 0
        self.gbifKey        = 0

        self.institutionId   = gs.institutionId #db.getRowOnId('collection',collection_id)['institutionid']
        self.collectionId    = collection_id

        self.taxonRanks = {
                    'PHYLUM':'30',
                    'CLASS':'60',
                    'ORDER':'100',
                    'FAMILY':'140',
                    'GENUS':'180',
                    'SPECIES':'220',
                    'SUBSPECIES':'230',
                    }

    def getFieldsAsDict(self):
        """
        Generates a dictonary with database column names as keys and specimen records fields as values 
        RETURNS said dictionary for passing on to data access handler 
        """
        
        fieldsDict = {
                'spid':f'"{self.spid}"', 
                'guid':f'"{self.guid}"',
                'name':f'"{self.name}"',
                'fullname':f'"{self.fullName}"',
                'author':f'"{self.author}"',
                'remarks':f'"{self.remarks}"',
                'rankid':f'{self.rankId}',
                'parentid':f'{self.parentId}',
                'highertaxonname':f'{self.parentFullName}',
                'duplicatespid':f'{self.duplicateSpid}',
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
        self.spid = record['spid']
        self.guid = record['guid']
        self.name = record['name']
        self.fullName = record['fullname']
        self.author = record['author']
        self.remarks = record['remarks']
        self.rankId = record['rankid']        
        self.parentId = record['parentid']            
        self.parentFullName = record['highertaxonname']  
        self.duplicateSpid = record['duplicatespid']
        self.parent = None
   
    def fill(self, jsonObject, source="Specify"):
        """
        Function for filling taxon model's fields with data from record fetched from external source
        CONTRACT 
            jsonObject (json)  : Data record fetched from external source
            source (String)    : String describing external source. 
                                 Options:
                                     "Specify = "Specify API 
        """
        self.source = source
        if jsonObject:
            if source=="Specify":
                self.spid = jsonObject['id'] # NOTE The 'id' of the Specify Object corresponds to the 'spid' field in the local app db
                self.guid = jsonObject['guid']
                self.name = jsonObject['name']
                self.fullName = jsonObject['fullname']
                self.author = jsonObject['author']
                self.remarks = jsonObject['remarks']
                self.rankId = jsonObject['rankid']        
                self.parentId = jsonObject['parent'].split('/')[4]
                self.parentFullName = '' # TODO Fetch parent full name 
                self.parent = Taxon(self.collectionId)
            elif source == "GBIF":
                self.gbifKey = jsonObject['key']
                self.guid = jsonObject['constituentKey']
                self.name = jsonObject['canonicalName'].split(' ').pop()
                self.fullName = jsonObject['canonicalName']
                self.author = jsonObject['authorship']
                self.remarks = jsonObject['remarks']
                self.rankId =  int(self.taxonRanks[jsonObject['rank']])
                self.parentFullName = jsonObject['parent']
                self.parent = Taxon(self.collectionId)
            else:
                self.remarks(f'Could not fill from unsupported source: "{source}"...')

    def loadPredefinedData(self):
        pass

    def getParent(self, specify_interface):
        self.parent = Taxon(self.collectionId)
        try:
            parentTaxonObj = specify_interface.getSpecifyObject(self.sptype, self.parentId)
            self.parent.fill(parentTaxonObj)
        except:
            print("ERROR: Failed to retrieve parent taxon.")
            pass
        return self.parent 

    def getParentage(self, specify_interface):
        # Recursive function for constructing the entire parent sequence down to "Life"
        done = False 
        current = self 
        while done != True: 
            temporary = current.getParent(specify_interface) 
            if (temporary.name == 'Life'): 
                done = True
            else: 
                current = temporary

    def __str__ (self):
        return f'id:{self.id}, spid:{self.spid}, name:"{self.name}", fullname:"{self.fullName}", author:"{self.author}", rankid:{self.rankId}, parentid: {self.parentId} '
