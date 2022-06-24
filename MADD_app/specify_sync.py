# -*- coding: utf-8 -*-
"""
  Created on Tuesday June 14, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Synchronizing local database with Specify 
"""
from getpass import getpass
import specify_interface as sp
import data_access as db
import util

def specifyLogin(baseURL, username, passwd):
    # TODO
    print('Connecting to Specify7 API...')
    sp.initInstitution(baseURL)
    csrftoken = sp.getCSRFToken()
    csrftoken = sp.login(username, passwd, csrftoken)
    if sp.verifySession(csrftoken):
        return csrftoken
    else:
        return '' 

def specifyLogout(csrftoken):
    # TODO
    print('logging out of Specify...')
    sp.logout(csrftoken)

def syncSpecifyCollections(csrftoken):
    # TODO
    print('Syncing collections with Specify...')
    specifyCollections = sp.fetchSpecifyObjects('collection', csrftoken)
    
    for i in range(0, len(specifyCollections)):
        spCollection = specifyCollections[i]
        print(' - checking for collection {%s,"%s"} in db:' %(spCollection['id'], spCollection['collectionname']))
        dbCollection = db.getRowsOnFilters('collections', {'spid': spCollection['id']})
        if(len(dbCollection)> 0):
            print(' - found')
        else:
            print(' - not found')
        pass

# TEST CODE
util.clear()
print('------- Running specify_sync.py --------')
institution = db.getRowOnId('institutions', 0)
# print(institution)
token = specifyLogin(institution[3], 'test', 'testtest') #input('Enter username: '), getpass('Enter password: '))
if token != '':
    syncSpecifyCollections(token)
else:
    print('Login failed...')
print('----------- done --------------')



"""
specifyCollections = sp.getInitialCollections()
#sp.
localdbCollections = db.getRows('collections')

for key in specifyCollections:
    print('checking for collection {%s,%s} in db:' %(key, specifyCollections[key]))
    if(len(db.getRowsOnFilters('collections', {'spid': key, 'name' : '"%s"' % specifyCollections[key]}))> 0):
        print('found')
    else:
        print('not found')
    pass
"""









