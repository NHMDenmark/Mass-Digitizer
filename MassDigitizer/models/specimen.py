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

from datetime import datetime
import pytz

# Internal dependencies
import data_access as db
import util

class specimen:
    # TODO description

    id = 0
    catalogNumber = ''
    multiSpecimen = ''
    taxonName = ''
    taxonNameid = 0
    typeStatusName = ''
    typeStatusId = 0
    geoRegionName = ''
    geoRegionId = 0
    storageId = ''
    storageName = ''
    storageId = 0
    prepTypeName = ''
    prepTypeId = 0
    notes = ''
    collectionId = 0
    userName = ''
    userId = 0
    workStation = ''
    recordDateTime = datetime.now()

    # Predefined data
    storageLocations = {}
    prepTypes = {}
    typeStatuses = {}
    geoRegions = {} 
    geoRegionSources = {}

    def __init__(self):
        pass

    def getFieldsAsDict(self):
        # TODO function contract 
        return {'catalognumber': '"%s"' % self.catalogNumber, # TODO "{}".format(var...)
                'multispecimen': '%s' % self.multiSpecimen,
                'taxonname': '"%s"' % self.taxonName,
                'taxonnameid': '%s' % util.getPrimaryKey(self.taxonName, 'fullname'),
                'typestatusid': '%s' % self.typeStatusId, 
                'georegionname': '"%s"' % self.geoRegionName,
                'georegionid': '%s' % self.geoRegionId, 
                'storagefullname': '"%s"' % self.storageFullName,
                'storagename': '"%s"' % self.storageName,
                'storageid': '%s' % self.storageId,
                'preptypename': '"%s"' % self.prepTypeName,
                'preptypeid': '%s' % self.prepTypeId,
                'notes': '"%s"' % self.notes,
                'collectionid': '%s' % self.collectionId,
                'username': '"%s"' % self.userName,
                'userid' : '%s' % util.getPrimaryKey(self.userName,'username'),
                'workstation': '"%s"' % self.workStation,
                'datetime': '"%s"' % datetime.now(),
                }

    def save(self):
        # TODO Function description & contract     
        # fields must be a dictionary with the specimen table headers as 'keys' and the form field content as 'values'.
        # insert is a switch to mark whether an INSERT or an UPDATE is called for.
        # recordID is required for updates.

        if id == 0:
            # Checking if Save is a novel record , or if it is updating existing record.
            print('We are inserting! ')
            print('Saving now ', datetime.now(pytz.timezone("Europe/Copenhagen")))
            sql_res = db.insertRow('specimen', self.getFieldsAsDict())
            return sql_res
        else:
            print('We are updating! ')
            print('the row with ID - ', self.id)
            update = db.updateRow('specimen', self.id, self.getFieldsAsDict())
            print(update)